# Upload retries

Uploads over 2 GB were failing because the retry loop restarted each upload from byte zero. A large file never finished inside the 10-minute job limit, so the job was killed and retried, and the cycle repeated until the queue gave up.

Retries now resume from the last confirmed chunk. The offset is stored by the chunk tracker after every successful write, and `resume_from_offset` in `upload.py` reads it back before the next attempt. A 5 GB test upload that failed on three attempts out of three now finishes in about four minutes.

But one case is still open. The S3-compatible store we use in staging reports offsets in a different unit, and I haven't tested against it. Worth checking before release.

## Deploying the change

The change needs a schema migration, because the tracker gains an `offset` column.

1. Run the migration from the repository root:

   ```sh
   ./scripts/migrate.sh 0042_add_chunk_offset
   ```

   It prints `applied 0042_add_chunk_offset` when it succeeds.

2. Restart the upload workers so they load the new code:

   ```sh
   systemctl restart upload-worker@*
   ```

3. Upload a file larger than 2 GB and watch the worker log. You should see `resumed from offset` lines if the connection drops during the upload.

If the migration fails with `relation "chunks" does not exist`, you're pointing at the wrong database. Check `DATABASE_URL` and try again.

## Open questions

The time to live (TTL) on stored offsets is seven days. That's long enough for any upload we've seen, but nobody chose it on purpose; it came from the tracker's default. We should decide whether to keep it.
