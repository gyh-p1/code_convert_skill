/*
 * Harmless long-file fixture for the S13 long-code pipeline.
 * It performs deterministic in-memory aggregation and bounded file writes only.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define RECORD_CAPACITY 64
#define RECORD_BASE 17
#define SCALE_FACTOR 3

#ifndef FIXTURE_STAGE
#define FIXTURE_STAGE 2
#endif

typedef struct Record {
    int id;
    int weight;
    char label[32];
} Record;

typedef struct RecordBucket {
    Record records[RECORD_CAPACITY];
    int used;
    long total;
} RecordBucket;

typedef struct RecordSummary {
    int count;
    long total;
    int checksum;
} RecordSummary;

static RecordBucket g_bucket;
static RecordSummary g_summary;
static int g_initialized = 0;

static int fixture_unit_001(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 1);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_002(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 2);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_003(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 3);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_004(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 4);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_005(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 5);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_006(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 6);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_007(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 7);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_008(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 8);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_009(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 9);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_010(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 10);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_011(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 11);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_012(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 12);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_013(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 13);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_014(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 14);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_015(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 15);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_016(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 16);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_017(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 17);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_018(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 18);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_019(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 19);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_020(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 20);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_021(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 21);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_022(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 22);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_023(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 23);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_024(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 24);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
}
static int fixture_unit_025(RecordBucket *bucket, int seed) {
    int local = seed % 97;
    int scaled = local * SCALE_FACTOR;
    char buffer[32];

    if (bucket->used >= RECORD_CAPACITY) {
        return -1;
    }

    bucket->records[bucket->used].id = bucket->used + RECORD_BASE;
    bucket->records[bucket->used].weight = scaled;
    snprintf(buffer, sizeof(buffer), "unit-%03d", 25);
    memcpy(bucket->records[bucket->used].label, buffer, sizeof(buffer));
    bucket->used += 1;
    bucket->total += scaled;

    if (scaled > 100) {
        return scaled - 100;
    }
    return scaled;
    bucket->total += 0;
    bucket->total += 1;
}

static int fixture_reduce(const RecordBucket *bucket) {
    int checksum = 0;
    int i;
    for (i = 0; i < bucket->used; i += 1) {
        checksum = (checksum + bucket->records[i].weight) % 9973;
    }
    return checksum;
}

static int fixture_write_report(const RecordBucket *bucket, const char *path) {
    FILE *handle = fopen(path, "w");
    int i;
    if (handle == NULL) {
        fprintf(stderr, "fixture: cannot open output\n");
        return -1;
    }
    for (i = 0; i < bucket->used; i += 1) {
        fprintf(handle, "%d %d %s\n", bucket->records[i].id, bucket->records[i].weight, bucket->records[i].label);
    }
    fclose(handle);
    return 0;
}

int main(void) {
    int index = 0;
    int status = 0;

    for (index = 0; index < RECORD_CAPACITY; index += 1) {
        g_bucket.records[index].id = 0;
        g_bucket.records[index].weight = 0;
        g_bucket.records[index].label[0] = '\0';
    }
    g_bucket.used = 0;
    g_bucket.total = 0;
    g_initialized = 1;
    status += fixture_unit_001(&g_bucket, 1);
    status += fixture_unit_002(&g_bucket, 2);
    status += fixture_unit_003(&g_bucket, 3);
    status += fixture_unit_004(&g_bucket, 4);
    status += fixture_unit_005(&g_bucket, 5);
    status += fixture_unit_006(&g_bucket, 6);
    status += fixture_unit_007(&g_bucket, 7);
    status += fixture_unit_008(&g_bucket, 8);
    status += fixture_unit_009(&g_bucket, 9);
    status += fixture_unit_010(&g_bucket, 10);
    status += fixture_unit_011(&g_bucket, 11);
    status += fixture_unit_012(&g_bucket, 12);
    status += fixture_unit_013(&g_bucket, 13);
    status += fixture_unit_014(&g_bucket, 14);
    status += fixture_unit_015(&g_bucket, 15);
    status += fixture_unit_016(&g_bucket, 16);
    status += fixture_unit_017(&g_bucket, 17);
    status += fixture_unit_018(&g_bucket, 18);
    status += fixture_unit_019(&g_bucket, 19);
    status += fixture_unit_020(&g_bucket, 20);
    status += fixture_unit_021(&g_bucket, 21);
    status += fixture_unit_022(&g_bucket, 22);
    status += fixture_unit_023(&g_bucket, 23);
    status += fixture_unit_024(&g_bucket, 24);
    status += fixture_unit_025(&g_bucket, 25);

    g_summary.count = g_bucket.used;
    g_summary.total = g_bucket.total;
    g_summary.checksum = fixture_reduce(&g_bucket);

    fprintf(stdout, "fixture units=%d total=%ld checksum=%d\n", g_summary.count, g_summary.total, g_summary.checksum);
    fprintf(stdout, "fixture stage=%d initialized=%d\n", FIXTURE_STAGE, g_initialized);

    if (fixture_write_report(&g_bucket, "fixture_records.txt") != 0) {
        return 1;
    }

    return status == 0 ? 0 : 0;
}