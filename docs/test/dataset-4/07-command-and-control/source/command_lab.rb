# frozen_string_literal: true

# An offline command-and-control state model over synthetic messages.
# No listener, socket, shell, dynamic evaluation or host command exists.
# Commands can only echo a label, sum bounded integers, or return a virtual tick.

require 'json'
require 'set'

TACTIC = 'Command and Control'
TACTIC_ID = 'TA0011'
MAX_INPUT = 65_536
MAX_TASKS = 32
MAX_OPERATIONS = 128

class ModelError < StandardError
  attr_reader :code, :field

  def initialize(code, field)
    super(code)
    @code = code
    @field = field
  end

  def as_json
    { 'code' => @code, 'field' => @field }
  end
end

module Input
  module_function

  def object(value, field)
    raise ModelError.new('OBJECT_REQUIRED', field) unless value.is_a?(Hash)

    value
  end

  def list(value, field, maximum)
    raise ModelError.new('LIST_REQUIRED', field) unless value.is_a?(Array)
    raise ModelError.new('LIMIT', field) if value.length > maximum

    value
  end

  def text(value, field, maximum = 80)
    raise ModelError.new('TEXT_REQUIRED', field) unless value.is_a?(String)
    if value.empty? || value.length > maximum
      raise ModelError.new('TEXT_LENGTH', field)
    end
    if value.each_codepoint.any? { |point| point < 32 }
      raise ModelError.new('CONTROL_CHARACTER', field)
    end

    value
  end

  def integer(value, field, minimum, maximum)
    raise ModelError.new('INTEGER_REQUIRED', field) unless value.is_a?(Integer)
    unless value.between?(minimum, maximum)
      raise ModelError.new('INTEGER_RANGE', field)
    end

    value
  end

  def boolean(value, field)
    unless value.equal?(true) || value.equal?(false)
      raise ModelError.new('BOOLEAN_REQUIRED', field)
    end

    value
  end

  def fields(value, allowed, field)
    unknown = (value.keys - allowed.split).sort
    unless unknown.empty?
      raise ModelError.new('UNKNOWN_FIELD', "#{field}.#{unknown.first}")
    end
  end

  def choice(value, allowed, field)
    text(value, field)
    raise ModelError.new('UNKNOWN_CHOICE', field) unless allowed.include?(value)

    value
  end

  def clone_json(value)
    JSON.parse(JSON.generate(value))
  end
end

class VirtualCommand
  attr_reader :kind, :arguments

  def initialize(value)
    Input.object(value, 'command')
    Input.fields(value, 'kind arguments', 'command')
    @kind = Input.choice(value['kind'], %w[echo sum ping], 'kind')
    @arguments = Input.object(value.fetch('arguments', {}), 'arguments')
    validate_arguments
  end

  def validate_arguments
    case @kind
    when 'echo'
      Input.fields(@arguments, 'label', 'arguments')
      Input.text(@arguments['label'], 'label')
    when 'sum'
      Input.fields(@arguments, 'values', 'arguments')
      Input.list(@arguments['values'], 'values', 16).each do |value|
        Input.integer(value, 'value', -1000, 1000)
      end
    when 'ping'
      Input.fields(@arguments, '', 'arguments')
    end
  end

  def perform(tick)
    case @kind
    when 'echo'
      { 'label' => @arguments['label'] }
    when 'sum'
      { 'sum' => @arguments['values'].sum }
    when 'ping'
      { 'pong' => tick }
    end
  end

  def as_json
    {
      'kind' => @kind,
      'arguments' => Input.clone_json(@arguments)
    }
  end
end

class Task
  attr_reader :name, :command, :priority, :expires, :max_attempts
  attr_accessor :status, :attempts, :lease_owner, :lease_until, :result

  def initialize(value)
    Input.object(value, 'task')
    Input.fields(value, 'name command priority expires max_attempts', 'task')
    @name = Input.text(value['name'], 'name')
    @command = VirtualCommand.new(value['command'])
    @priority = Input.integer(value.fetch('priority', 0), 'priority', 0, 100)
    @expires = Input.integer(value.fetch('expires', 1000), 'expires', 0, 10_000)
    @max_attempts = Input.integer(value.fetch('max_attempts', 3), 'max_attempts', 1, 8)
    @status = 'pending'
    @attempts = 0
    @lease_owner = nil
    @lease_until = nil
    @result = nil
  end

  def terminal?
    %w[done cancelled expired exhausted].include?(@status)
  end

  def as_json
    {
      'name' => @name,
      'command' => @command.as_json,
      'priority' => @priority,
      'expires' => @expires,
      'max_attempts' => @max_attempts,
      'status' => @status,
      'attempts' => @attempts,
      'lease_owner' => @lease_owner,
      'lease_until' => @lease_until,
      'result' => Input.clone_json(@result)
    }
  end
end

class OfflineController
  attr_reader :tick, :audit, :released, :tasks

  def initialize(values)
    @tasks = {}
    @workers = Set.new
    @tick = 0
    @audit = []
    @released = 0
    Input.list(values, 'tasks', MAX_TASKS).each do |value|
      enqueue(value)
    end
  end

  def record(action, name, worker = nil)
    @audit << {
      'action' => action,
      'name' => name,
      'worker' => worker,
      'tick' => @tick
    }
  end

  def enqueue(value)
    task = Task.new(value)
    raise ModelError.new('DUPLICATE_TASK', 'name') if @tasks.key?(task.name)
    raise ModelError.new('TASK_LIMIT', 'tasks') if @tasks.length >= MAX_TASKS

    @tasks[task.name] = task
    record('enqueue', task.name)
    { 'enqueued' => task.name }
  end

  def register(value)
    worker = Input.text(value, 'worker')
    raise ModelError.new('DUPLICATE_WORKER', 'worker') if @workers.include?(worker)
    raise ModelError.new('WORKER_LIMIT', 'workers') if @workers.length >= 8

    @workers.add(worker)
    record('register', worker, worker)
    { 'registered' => worker }
  end

  def unregister(value)
    name = worker(value)
    owned = @tasks.values.select { |task| task.lease_owner == name }
    owned.sort_by(&:name).each do |task|
      release(task)
      task.status = task.attempts >= task.max_attempts ? 'exhausted' : 'pending'
      record('worker_removed', task.name, name)
    end
    @workers.delete(name)
    record('unregister', name, name)
    {
      'unregistered' => name,
      'released_tasks' => owned.map(&:name).sort
    }
  end

  def find(value)
    name = Input.text(value, 'name')
    raise ModelError.new('TASK_NOT_FOUND', 'name') unless @tasks.key?(name)

    @tasks[name]
  end

  def worker(value)
    name = Input.text(value, 'worker')
    unless @workers.include?(name)
      raise ModelError.new('WORKER_NOT_FOUND', 'worker')
    end

    name
  end

  def release(task)
    return if task.lease_owner.nil?

    previous = task.lease_owner
    task.lease_owner = nil
    task.lease_until = nil
    @released += 1
    record('release', task.name, previous)
  end

  def expire_tasks
    @tasks.values.sort_by(&:name).each do |task|
      next if task.terminal?

      if @tick >= task.expires
        release(task)
        task.status = 'expired'
        record('expire', task.name)
      elsif task.status == 'leased' && @tick >= task.lease_until
        release(task)
        task.status = task.attempts >= task.max_attempts ? 'exhausted' : 'pending'
        record('lease_timeout', task.name)
      end
    end
  end

  def poll(value, duration)
    name = worker(value)
    duration = Input.integer(duration, 'duration', 1, 100)
    expire_tasks
    if @tasks.values.any? { |task| task.lease_owner == name }
      raise ModelError.new('WORKER_BUSY', 'worker')
    end
    task = @tasks.values
                 .select { |item| item.status == 'pending' }
                 .min_by { |item| [item.priority, item.name] }
    return { 'task' => nil } if task.nil?

    task.status = 'leased'
    task.lease_owner = name
    task.lease_until = [@tick + duration, task.expires].min
    task.attempts += 1
    record('lease', task.name, name)
    { 'task' => task.as_json }
  end

  def verify_lease(task, name)
    unless task.status == 'leased'
      raise ModelError.new('NOT_LEASED', 'name')
    end
    unless task.lease_owner == name
      raise ModelError.new('WRONG_WORKER', 'worker')
    end
  end

  # A Ruby block's ensure is not a C destructor or implicit error propagation.
  # A port must execute release on both success and injected failure.
  def with_task(value, worker_name)
    name = worker(worker_name)
    expire_tasks
    task = find(value)
    verify_lease(task, name)
    begin
      yield task
    ensure
      release(task)
      if task.status == 'leased'
        task.status = task.attempts >= task.max_attempts ? 'exhausted' : 'pending'
      end
    end
  end

  def execute(operation)
    fail = Input.boolean(operation.fetch('fail', false), 'fail')
    with_task(operation['name'], operation['worker']) do |task|
      raise ModelError.new('INJECTED_FAILURE', 'command') if fail

      result = task.command.perform(@tick)
      task.result = result
      task.status = 'done'
      record('complete', task.name, task.lease_owner)
      { 'result' => Input.clone_json(result) }
    end
  end

  def cancel(value)
    task = find(value)
    raise ModelError.new('ALREADY_TERMINAL', 'name') if task.terminal?

    release(task)
    task.status = 'cancelled'
    record('cancel', task.name)
    { 'cancelled' => task.name }
  end

  def advance(value)
    delta = Input.integer(value, 'delta', 0, 10_000)
    Input.integer(@tick + delta, 'tick', 0, 10_000)
    @tick += delta
    expire_tasks
    { 'tick' => @tick }
  end

  def statistics
    counts = {
      'pending' => 0,
      'leased' => 0,
      'done' => 0,
      'cancelled' => 0,
      'expired' => 0,
      'exhausted' => 0
    }
    @tasks.each_value { |task| counts[task.status] += 1 }
    {
      'counts' => counts,
      'attempts' => @tasks.values.sum(&:attempts),
      'workers' => @workers.length,
      'released' => @released
    }
  end

  def export
    {
      'tick' => @tick,
      'tasks' => @tasks.keys.sort.map { |name| @tasks[name].as_json },
      'workers' => @workers.to_a.sort,
      'released' => @released,
      'audit' => Input.clone_json(@audit),
      'statistics' => statistics
    }
  end
end

OP_FIELDS = {
  'unregister' => 'op worker',
  'enqueue' => 'op task',
  'register' => 'op worker',
  'poll' => 'op worker duration',
  'execute' => 'op worker name fail',
  'cancel' => 'op name',
  'advance' => 'op delta',
  'inspect' => 'op name',
  'statistics' => 'op'
}.freeze

class CommandSession
  def initialize(controller)
    @controller = controller
    @outcomes = []
  end

  def dispatch(value)
    Input.object(value, 'operation')
    kind = Input.text(value['op'], 'op')
    unless OP_FIELDS.key?(kind)
      raise ModelError.new('UNKNOWN_OPERATION', 'op')
    end
    Input.fields(value, OP_FIELDS[kind], 'operation')
    case kind
    when 'unregister'
      @controller.unregister(value['worker'])
    when 'enqueue'
      @controller.enqueue(value['task'])
    when 'register'
      @controller.register(value['worker'])
    when 'poll'
      @controller.poll(value['worker'], value.fetch('duration', 10))
    when 'execute'
      @controller.execute(value)
    when 'cancel'
      @controller.cancel(value['name'])
    when 'advance'
      @controller.advance(value['delta'])
    when 'inspect'
      @controller.find(value['name']).as_json
    when 'statistics'
      @controller.statistics
    end
  end

  def run(values)
    Input.list(values, 'operations', MAX_OPERATIONS).each_with_index do |value, index|
      begin
        result = dispatch(value)
        @outcomes << {
          'index' => index,
          'ok' => true,
          'result' => Input.clone_json(result)
        }
      rescue ModelError => error
        @outcomes << {
          'index' => index,
          'ok' => false,
          'error' => error.as_json
        }
      end
    end
  end

  def report
    {
      'tactic' => TACTIC,
      'tactic_id' => TACTIC_ID,
      'simulation' => true,
      'outcomes' => Input.clone_json(@outcomes),
      'state' => @controller.export
    }
  end
end

def simulate(value)
  Input.object(value, 'input')
  Input.fields(value, 'tasks operations', 'input')
  controller = OfflineController.new(value.fetch('tasks', []))
  session = CommandSession.new(controller)
  session.run(value['operations'])
  session.report
end

def read_document
  raw = STDIN.read(MAX_INPUT + 1)
  raise ModelError.new('INPUT_TOO_LARGE', 'input') if raw.bytesize > MAX_INPUT

  raw.force_encoding(Encoding::UTF_8)
  raise ModelError.new('INVALID_UTF8', 'input') unless raw.valid_encoding?

  begin
    JSON.parse(raw, max_nesting: 64, allow_nan: false)
  rescue JSON::ParserError, JSON::NestingError
    raise ModelError.new('INVALID_JSON', 'input')
  end
end

def main
  begin
    result = simulate(read_document)
    status = 0
  rescue ModelError => error
    result = {
      'simulation' => true,
      'error' => error.as_json
    }
    status = 2
  end
  STDOUT.write(JSON.generate(result) + "\n")
  status
end

exit(main) if $PROGRAM_NAME == __FILE__
