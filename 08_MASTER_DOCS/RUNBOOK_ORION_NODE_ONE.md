# Orion Node One — Runbook (Ed25519 / JSONL)

This runbook activates the signed heartbeat and append-only feed using pure Ed25519 (NaCl) via OpenSSL, no third-party deps.

Paths used:
- Identity: `/.well-known/orion/identity.json`
- Heartbeat: `/.well-known/orion/status.json`
- Peers: `/.well-known/orion/peers.json`
- Feed: `/orion/feed.jsonl`
- Tools: `scripts/orion_sign.sh`, `scripts/orion_tools.py`

## 0) Threat model and roles
- Offline root key (root): created and stored off the node (air-gapped). Used only to bind/approve signer keys.
- Online signing key (signer): lives on this node, used to sign `status.json` and feed entries.

## 1) Generate keys

1. Root (offline, air-gapped machine):
   - `openssl genpkey -algorithm Ed25519 -out root_sk.pem`
   - `openssl pkey -in root_sk.pem -pubout -out root_pk.pem`
   - `openssl pkey -pubin -in root_pk.pem -outform DER | sha256sum | awk '{print $1}'`

2. Signer (on this node):
   - `./scripts/orion_sign.sh gen-key keys/signing`
   - `./scripts/orion_sign.sh fingerprint keys/signing/pk.pem`

Record both fingerprints. Keep `root_sk.pem` offline. Never copy it to this node.

## 2) Fill identity.json and bind signer

1. Paste `root_pk.pem` and `keys/signing/pk.pem` PEM contents into `/.well-known/orion/identity.json` under `roles.root.pubkey_pem` and `roles.signer.pubkey_pem` respectively.
2. Compute fingerprints and fill `roles.*.fingerprint`.
   - Root FP (offline): `openssl pkey -pubin -in root_pk.pem -outform DER | sha256sum | awk '{print $1}'`
   - Signer FP (online): `./scripts/orion_sign.sh fingerprint keys/signing/pk.pem`
3. Create binding message on the offline machine (same format as in identity.json):
   - `printf 'orion-node-1|<SIGNER_FP>|%s' 2025-11-08 > msg.txt`
   - `openssl pkeyutl -sign -inkey root_sk.pem -rawin -in msg.txt -out bind.sig`
   - `base64 -w0 bind.sig > bind.sig.b64`
4. Paste base64 into `identity.json.signer_binding.sig` and set `REPLACE_WITH_ONLINE_SIGNER_FPR` to the actual FP.

Commit or deploy the updated `identity.json` to this node.

## 3) Append signed feed entries

Append a boot entry (example metadata shown):

```bash
./scripts/orion_sign.sh append keys/signing/sk.pem orion/feed.jsonl node_boot '{"version":1,"source":"runbook"}'
```

Append any operational event later (example):

```bash
./scripts/orion_sign.sh append keys/signing/sk.pem orion/feed.jsonl opsec_update '{"doc":"opsec.html","rev":"2025-11-08"}'
```

Feed lines are canonicalized, hashed (sha256), chained via `prev`, and signed by the signer key.

## 4) Produce signed heartbeat

Generate a signed `status.json` reflecting current head:

```bash
./scripts/orion_sign.sh status keys/signing/sk.pem orion/feed.jsonl .well-known/orion/status.json
```

This updates `state: online`, `epoch`, `timestamp`, `head`, and `sig`.

## 5) Verify signatures

1. Verify heartbeat:

```bash
SIG=$(jq -r .sig .well-known/orion/status.json)
./scripts/orion_sign.sh verify-json keys/signing/pk.pem .well-known/orion/status.json "$SIG"
```

2. Verify last feed line:

```bash
tail -n 1 orion/feed.jsonl > /tmp/last.json
jq -r .sig /tmp/last.json | tr -d '\n' > /tmp/sig.b64
jq 'del(.sig,.hash)' /tmp/last.json > /tmp/unsigned.json
SIG=$(cat /tmp/sig.b64)
./scripts/orion_sign.sh verify-json keys/signing/pk.pem /tmp/unsigned.json "$SIG"
```

## 6) Rotation

1. Generate a new signer keypair on the node.
2. Offline root signs a new binding for the new signer fingerprint.
3. Update `identity.json.roles.signer` and `signer_binding`.
4. Append a `key_rotation` event to the feed with both old and new fingerprints.

```bash
./scripts/orion_sign.sh append keys/signing/sk.pem orion/feed.jsonl key_rotation '{"old":"<OLD_FP>","new":"<NEW_FP>"}'
```

## 7) Peers and mirrors

- Keep `/.well-known/orion/peers.json` empty in Phase 1.
- To mirror, rsync `/.well-known/orion/` and `/orion/` to read-only hosts.

## 8) Incident response

- Compromise of signer: revoke by publishing updated `identity.json` (new signer) and append `key_rotation` + `incident` event in feed.
- Compromise of root: rebuild trust root and publish a fresh `identity.json` with explicit declaration; announce via out-of-band channels.

