// Measure the public site only; local previews make no analytics requests.
if (location.protocol === "https:" && ["yaqyn.dev", "www.yaqyn.dev"].includes(location.hostname)) {
  const beacon = document.createElement("script");
  beacon.src = "https://static.cloudflareinsights.com/beacon.min.js";
  beacon.defer = true;
  beacon.dataset.cfBeacon = JSON.stringify({ token: "ca583c29e7b7467f964abcbf0279066d" });
  document.body.appendChild(beacon);
}
