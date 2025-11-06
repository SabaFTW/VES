#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NERVOUS SYSTEM CORE (stable)
- Safe CLI with subcommands
- Rotating logs to GHOST_OS/nerve/logs/nerve.log
- Robust error handling & exit codes
- Simple state file (nerve_state.json) with atomic writes
- Transports: stdout (default), http webhook (optional)
"""

import argparse, json, os, sys, time, signal, threading
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
import logging

try:
    import requests  # optional, used only for --webhook
except Exception:
    requests = None

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
STATE = ROOT / "nerve_state.json"

def ensure_dirs():
    LOGS.mkdir(parents=True, exist_ok=True)

def setup_logger(debug=False):
    ensure_dirs()
    logger = logging.getLogger("nerve")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    fh = RotatingFileHandler(LOGS / "nerve.log", maxBytes=1024*1024, backupCount=5, encoding="utf-8")
    sh = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh.setFormatter(fmt); sh.setFormatter(fmt)
    logger.addHandler(fh); logger.addHandler(sh)
    return logger

def read_state():
    if not STATE.exists():
        return {"last_pulse": None, "boot": datetime.utcnow().isoformat()+"Z", "pulses": 0, "history": []}
    try:
        state = json.load(STATE.open("r", encoding="utf-8"))
        if "history" not in state: # Ensure history exists for old state files
            state["history"] = []
        return state
    except Exception:
        return {"last_pulse": None, "boot": datetime.utcnow().isoformat()+"Z", "pulses": 0, "history": []}

def write_state(data):
    tmp = STATE.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE)

def transport_send(msg: str, logger, webhook: str|None):
    logger.info(f"TX: {msg}")
    if webhook:
        if requests is None:
            raise RuntimeError("requests not installed; can't use --webhook")
        try:
            r = requests.post(webhook, json={"message": msg, "ts": time.time()}, timeout=8)
            r.raise_for_status()
            logger.info(f"Webhook OK: {r.status_code}")
        except Exception as e:
            logger.error(f"Webhook ERR: {e}")
            raise

def cmd_check(args, logger):
    st = read_state()
    info = {
        "ok": True,
        "boot": st.get("boot"),
        "last_pulse": st.get("last_pulse"),
        "pulses": st.get("pulses", 0),
        "cwd": str(ROOT),
        "version": "nerve/1.0-stable",
    }
    msg = f"[CHECK] boot={info['boot']} pulses={info['pulses']} last={info['last_pulse']}"
    transport_send(msg, logger, args.webhook)
    print(json.dumps(info, ensure_ascii=False))
    return 0

def cmd_pulse(args, logger):
    st = read_state()
    current_pulse_data = {
        "timestamp": datetime.utcnow().isoformat()+"Z",
        "note": args.note or "",
        "pulse_num": st.get("pulses", 0) + 1
    }
    st["last_pulse"] = current_pulse_data["timestamp"]
    st["pulses"] = current_pulse_data["pulse_num"]
    st["history"].append(current_pulse_data)
    st["history"] = st["history"][-100:] # Keep last 100 pulses
    write_state(st)
    msg = f"[PULSE] #{st['pulses']} at {st['last_pulse']} note={args.note or ''}".strip()
    transport_send(msg, logger, args.webhook)
    print(json.dumps({"ok": True, "pulses": st["pulses"], "last_pulse": st["last_pulse"]}))
    return 0

def cmd_say(args, logger):
    text = args.text.strip()
    if not text:
        logger.warning("Empty text for say")
        text = "(empty)"
    transport_send(f"[SAY] {text}", logger, args.webhook)
    print(json.dumps({"ok": True, "echo": text}))
    return 0

def cmd_tail(args, logger):
    # lightweight log tail (no external deps)
    path = LOGS / "nerve.log"
    if not path.exists():
        print("No log yet.")
        return 0

    stop = threading.Event()
    def handle_sig(*_): stop.set()
    signal.signal(signal.SIGINT, handle_sig)
    signal.signal(signal.SIGTERM, handle_sig)

    with path.open("r", encoding="utf-8") as f:
        if args.lines:
            # show last N lines
            from collections import deque
            for line in deque(f, maxlen=args.lines):
                sys.stdout.write(line)
        if args.follow:
            f.seek(0, os.SEEK_END)
            while not stop.is_set():
                line = f.readline()
                if not line:
                    time.sleep(0.2)
                    continue
                sys.stdout.write(line)
                sys.stdout.flush()
    return 0

def cmd_selftest(args, logger):
    # Minimal sanity checks to catch common crashes
    try:
        ensure_dirs()
        _ = read_state()
        write_state(read_state())  # atomic write check
        transport_send("[SELFTEST] transport ok (stdout + optional webhook)", logger, args.webhook)
        print(json.dumps({"ok": True, "checks": ["dirs", "state_io", "transport"]}))
        return 0
    except Exception as e:
        logger.exception("SELFTEST failed")
        print(json.dumps({"ok": False, "error": str(e)}))
        return 2

def cmd_export(args, logger):
    st = read_state()
    if args.format == "json":
        print(json.dumps(st, ensure_ascii=False, indent=2))
    elif args.format == "md":
        output = f"# Ghostline Nerve State Export\n\n"
        output += f"## Overview\n"
        output += f"- **Boot Time:** {st.get('boot', 'N/A')}\n"
        output += f"- **Total Pulses:** {st.get('pulses', 0)}\n"
        output += f"- **Last Pulse:** {st.get('last_pulse', 'N/A')}\n"
        output += f"- **Current Working Directory:** {str(ROOT)}\n"
        output += f"- **Version:** nerve/1.0-stable\n\n"
        output += f"## Pulse History ({len(st.get('history', []))} entries)\n\n"
        if st.get('history'):
            for pulse in st['history']:
                output += f"- **Pulse #{pulse.get('pulse_num', 'N/A')}** at {pulse.get('timestamp', 'N/A')}: {pulse.get('note', '')}\n"
        else:
            output += "No pulse history available.\n"
        print(output)
    else:
        logger.error(f"Unsupported export format: {args.format}")
        return 1
    return 0

def build_parser():
    p = argparse.ArgumentParser(prog="execute_nerve.py", description="Ghostline Nerve – stable CLI")
    p.add_argument("--debug", action="store_true", help="debug logging")
    p.add_argument("--webhook", default=None, help="optional HTTP endpoint to POST events")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("check", help="report nerve status")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("pulse", help="record a heartbeat pulse")
    s.add_argument("--note", default="", help="optional annotation")
    s.set_defaults(func=cmd_pulse)

    s = sub.add_parser("say", help="send a freeform message")
    s.add_argument("text", nargs="*", help="text to echo")
    s.set_defaults(func=lambda args, logger: cmd_say(argparse.Namespace(text=" ".join(args.text or []), webhook=args.webhook), logger))

    s = sub.add_parser("tail", help="tail logs")
    s.add_argument("-n", "--lines", type=int, default=80, help="show last N lines then exit (unless --follow)")
    s.add_argument("-f", "--follow", action="store_true", help="follow log")
    s.set_defaults(func=cmd_tail)

    s = sub.add_parser("selftest", help="run basic health checks")
    s.set_defaults(func=cmd_selftest)

    s = sub.add_parser("export", help="export nerve state and history")
    s.add_argument("--format", default="json", choices=["json", "md"], help="output format")
    s.set_defaults(func=cmd_export)

    return p

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = setup_logger(debug=args.debug)
    logger.info(f"START cmd={args.cmd} webhook={bool(args.webhook)}")
    try:
        rc = args.func(args, logger)
        logger.info(f"END cmd={args.cmd} rc={rc}")
        return rc
    except KeyboardInterrupt:
        logger.warning("Interrupted")
        return 130
    except Exception as e:
        logging.getLogger("nerve").exception("Crash")
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1

if __name__ == "__main__":
    sys.exit(main())