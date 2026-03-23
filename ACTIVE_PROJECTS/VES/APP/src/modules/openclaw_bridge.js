const BRIDGE_CONFIG = {
  lanVesUrl: "http://192.168.1.243:3000/",
  tailnetVesUrl: "http://100.64.64.104:3000/",
  nextcloudUrl: "https://arch.tailcd4edb.ts.net/",
  localGatewayUrl: "http://127.0.0.1:18789/",
  webhookUrl: "http://127.0.0.1:8788/nextcloud-talk-webhook",
};

function setLink(id, href, label = href) {
  const node = document.getElementById(id);
  if (!node) {
    return;
  }
  node.href = href;
  node.textContent = label;
}

export function initOpenClawBridge() {
  setLink("bridge-current-link", window.location.href, window.location.origin);
  setLink("bridge-lan-link", BRIDGE_CONFIG.lanVesUrl);
  setLink("bridge-tailnet-link", BRIDGE_CONFIG.tailnetVesUrl);
  setLink("bridge-nextcloud-link", BRIDGE_CONFIG.nextcloudUrl, "arch.tailcd4edb.ts.net");

  const gatewayNode = document.getElementById("bridge-gateway-url");
  const webhookNode = document.getElementById("bridge-webhook-url");
  const statusNode = document.getElementById("bridge-status");
  const controlLink = document.getElementById("bridge-control-link");
  const controlHint = document.getElementById("bridge-control-hint");

  if (gatewayNode) {
    gatewayNode.textContent = BRIDGE_CONFIG.localGatewayUrl;
  }

  if (webhookNode) {
    webhookNode.textContent = BRIDGE_CONFIG.webhookUrl;
  }

  if (statusNode) {
    statusNode.textContent = "VES portal is live. OpenClaw gateway stays on the Arch host as the local ops/control lane.";
  }

  const isHostLocal =
    window.location.hostname === "127.0.0.1" ||
    window.location.hostname === "localhost";

  if (isHostLocal) {
    controlLink?.classList.remove("hidden");
    if (controlLink instanceof HTMLAnchorElement) {
      controlLink.href = BRIDGE_CONFIG.localGatewayUrl;
    }
    if (controlHint) {
      controlHint.textContent = "Control UI is available directly on this host.";
    }
  } else {
    controlLink?.classList.add("hidden");
    if (controlHint) {
      controlHint.textContent =
        "Control UI is local-only right now because OpenClaw binds to loopback. For phone use VES via LAN/Tailnet and keep OpenClaw ops on the Arch host.";
    }
  }
}
