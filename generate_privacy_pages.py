#!/usr/bin/env python3
"""Generate account privacy-policy pages from the canonical mapdata.json.

Usage:
    python3 generate_privacy_pages.py /path/to/mapdata.json
    python3 generate_privacy_pages.py --check /path/to/mapdata.json
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


SITE_ROOT = Path(__file__).resolve().parent
LAST_UPDATED = "29 August 2026"

ACCOUNT_PAGES = {
    "kalan300": ("KV Maps", "privacy-kvmaps.html"),
    "kalanvishwanath": ("Minima", "privacy-minima.html"),
    "gamiya.net": ("Gamiya", "privacy-gamiya.html"),
    "kvnavaratna": ("Gamiya Four", "privacy-gamiya-four.html"),
    "kalan.nawarathne": ("Gamiya Two", "privacy-gamiya-two.html"),
}


def escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def policy_sections(subject: str, plural: bool) -> str:
    noun = "applications" if plural else "application"
    subject_ref = "These applications" if plural else "This application"
    download_verb = "do" if plural else "does"
    use_verb = "use" if plural else "uses"
    require_verb = "do" if plural else "does"
    security_subject = "the applications limit" if plural else "the application limits"
    return f"""
      <section aria-labelledby="on-device">
        <h2 id="on-device">Information stored on your device</h2>
        <ul>
          <li>Location is used, with your permission, to show your position, find nearby places, calculate routes, and provide active navigation.</li>
          <li>Downloaded maps, routing data, place and transit data, application preferences, and search history are stored in the application's private storage.</li>
          <li>You can remove downloaded content in Settings where that option is available. Clearing application storage or uninstalling the application removes its on-device data.</li>
        </ul>
      </section>

      <section aria-labelledby="downloads">
        <h2 id="downloads">Map and navigation downloads</h2>
        <p>Depending on the features available, the {noun} may request manifests, map tiles, routing data, place indexes, travel-guide content, and transit datasets from hosting and content-delivery providers, including Cloudflare R2-backed services. Like ordinary internet requests, those providers may receive technical metadata such as your IP address, request time, requested file, and user-agent information.</p>
        <p>{subject_ref} {download_verb} not include your saved search history or precise GPS position in content-download requests.</p>
      </section>

      <section aria-labelledby="advertising">
        <h2 id="advertising">Advertising and consent</h2>
        <p>The {noun} {use_verb} Google Mobile Ads. Google and its advertising partners may process device or advertising identifiers, IP address, general location derived from the network, ad interactions, consent choices, and diagnostics, subject to your device settings, applicable law, and available consent controls.</p>
        <p>See <a href="https://policies.google.com/privacy">Google's Privacy Policy</a> and <a href="https://policies.google.com/technologies/ads">How Google uses information for advertising</a>.</p>
      </section>

      <section aria-labelledby="developer-information">
        <h2 id="developer-information">Information received by the developer</h2>
        <p>The {noun} {require_verb} not require an account, and {subject} does not operate a location-history or search-history backend for {"them" if plural else "it"}. The developer may receive aggregated advertising, usage, and application-performance reports supplied by service providers. Depending on the application version and configuration, Google Firebase components may process app-instance identifiers, device information, application interactions, and diagnostics under Google's policies.</p>
        <p>Some application versions may offer a fuel-information contribution feature. If you deliberately submit an update, the fuel details, related place identifier and coordinates, and submission time are sent to Google Firebase/Firestore to provide that feature. The submission is not linked to an in-app user account or to your saved search history.</p>
      </section>

      <section aria-labelledby="permissions">
        <h2 id="permissions">Permissions</h2>
        <ul>
          <li><strong>Location:</strong> supports positioning, nearby search, route-start selection, and navigation. When active navigation is available, location may continue to be used after the application moves to the background.</li>
          <li><strong>Notifications:</strong> where requested, supports active-navigation and offline-download progress notifications.</li>
          <li><strong>Network access:</strong> supports content downloads, advertising, consent messages, and any online features described above.</li>
        </ul>
      </section>

      <section aria-labelledby="retention">
        <h2 id="retention">Retention and service providers</h2>
        <p>On-device data remains until you remove it, clear application storage, or uninstall the application. Hosting, advertising, analytics, and Firebase providers retain technical, advertising, diagnostic, or deliberately submitted data according to their own policies and legal obligations.</p>
      </section>

      <section aria-labelledby="security">
        <h2 id="security">Data security</h2>
        <p>Network data is transmitted to the service providers described above using encrypted HTTPS/TLS connections. On-device application data is kept in Android application storage. No storage or transmission method is completely secure, but {security_subject} data handling to what is needed for available features and service-provider integrations.</p>
      </section>

      <section aria-labelledby="choices">
        <h2 id="choices">Your choices</h2>
        <p>You can decline optional permissions, change location and notification permissions in Android settings, use available advertising-consent controls, remove downloaded content, clear application storage, or uninstall the application. Some features will not work without the permissions or network access they require.</p>
      </section>

      <section aria-labelledby="changes">
        <h2 id="changes">Changes to this policy</h2>
        <p>This policy may be updated when application features or service providers change. The current version and its last-updated date are published on this page.</p>
      </section>

      <section aria-labelledby="contact">
        <h2 id="contact">Contact</h2>
        <p>Questions or privacy requests can be sent to <a href="mailto:gamiya.net@gmail.com">gamiya.net@gmail.com</a>.</p>
      </section>"""


def page_shell(title: str, header: str, intro: str, content: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Privacy policy for {escape(title)}.">
    <title>{escape(title)} - Privacy Policy</title>
    <link rel="stylesheet" href="stylesheets/normalize.css">
    <link rel="stylesheet" href="stylesheets/stylesheet.css">
    <link rel="stylesheet" href="stylesheets/privacy-policy.css">
  </head>
  <body>
    <header class="page-header">
      <h1 class="project-name">{escape(header)}</h1>
      <p class="project-tagline">Privacy Policy</p>
    </header>

    <main class="main-content policy-content">
      <p class="last-updated">Last updated: {LAST_UPDATED}</p>
      {intro}
{content}
    </main>
  </body>
</html>
"""


def account_page(brand: str, apps: list[dict[str, Any]]) -> str:
    app_items = []
    for app in sorted(apps, key=lambda item: (item["app_name_field"].casefold(), item["bundle_id"])):
        app_items.append(
            "          <li><strong>"
            + escape(app["app_name_field"])
            + "</strong><code>"
            + escape(app["bundle_id"])
            + "</code></li>"
        )

    intro = (
        f'<p>This policy applies to the {len(apps)} offline map and navigation applications '
        f'published through the {escape(brand)} Google Play developer account and listed below. '
        "They are designed for offline use: map rendering, route calculation, downloaded content, "
        "and saved search history are primarily processed and stored on your device. Network "
        "connections still occur for downloads, advertising, and certain optional features as "
        "described in this policy.</p>"
    )
    covered = f"""
      <section aria-labelledby="covered-apps">
        <h2 id="covered-apps">Apps covered by this policy</h2>
        <ul class="app-list">
{chr(10).join(app_items)}
        </ul>
      </section>
"""
    return page_shell(
        f"{brand} Offline Map Apps",
        f"{brand} Offline Map Apps",
        intro,
        covered + policy_sections(brand, plural=True),
    )


def world_map_page() -> str:
    intro = (
        '<p>This policy applies to <strong>KV Offline World Maps</strong> (shown in the app as KV Maps), '
        'the offline world map and navigation application with package ID '
        '<code>com.kvmaps.worldmap</code>. The application is '
        "designed for offline use: map rendering, route calculation, downloaded content, and saved "
        "search history are primarily processed and stored on your device. Network connections still "
        "occur for downloads, advertising, and certain optional features as described in this policy.</p>"
    )
    return page_shell(
        "KV Offline World Maps",
        "KV Offline World Maps",
        intro,
        policy_sections("the developer", plural=False),
    )


def expected_pages(mapdata_path: Path) -> dict[str, str]:
    data = json.loads(mapdata_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("mapdata.json must contain a JSON array")

    pages: dict[str, str] = {}
    for account, (brand, filename) in ACCOUNT_PAGES.items():
        apps = [item for item in data if item.get("account") == account]
        if not apps:
            raise ValueError(f"No applications found for account {account!r}")
        for app in apps:
            if not app.get("bundle_id") or not app.get("app_name_field"):
                raise ValueError(f"Incomplete application record for account {account!r}: {app!r}")
        pages[filename] = account_page(brand, apps)

    pages["privacy-worldmap.html"] = world_map_page()
    return pages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mapdata", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    pages = expected_pages(args.mapdata.resolve())
    changed = []
    for filename, expected in pages.items():
        destination = SITE_ROOT / filename
        current = destination.read_text(encoding="utf-8") if destination.exists() else None
        if current != expected:
            changed.append(filename)
            if not args.check:
                destination.write_text(expected, encoding="utf-8")

    data = json.loads(args.mapdata.read_text(encoding="utf-8"))
    assigned = sum(1 for item in data if item.get("account") in ACCOUNT_PAGES)
    unassigned = sum(1 for item in data if not item.get("account"))
    print(f"Generated coverage: {assigned} assigned apps; {unassigned} unassigned records skipped")

    if args.check and changed:
        print("Out-of-date pages: " + ", ".join(changed))
        return 1
    if changed and not args.check:
        print("Updated pages: " + ", ".join(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
