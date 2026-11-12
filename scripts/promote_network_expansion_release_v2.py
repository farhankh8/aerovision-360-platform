
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import os

ROOT = Path(__file__).resolve().parents[1]

PACKAGE = (
    ROOT / "reports" / "network_expansion_20261104"
    / "deployment_package_v2"
)

BASE = ROOT / "reports" / "network_expansion_20261104"
EXECUTIONS = BASE / "promotion_execution"

EXPECTED_TARGETS = {
    "data/03_curated/dim_airport.csv",
    "data/03_curated/dim_airport.parquet",
    "data/03_curated/dim_route.csv",
    "data/03_curated/dim_route.parquet",
    "data/manifests/dim_airport_manifest.json",
    "data/manifests/dim_route_manifest.json",
    "scripts/build_dim_airport.py",
    "scripts/build_dim_route.py",
    "scripts/audit_dimensions.py"
}

TARGET_ORDER = [
    "data/03_curated/dim_airport.csv",
    "data/03_curated/dim_airport.parquet",
    "data/03_curated/dim_route.csv",
    "data/03_curated/dim_route.parquet",
    "data/manifests/dim_airport_manifest.json",
    "data/manifests/dim_route_manifest.json",
    "scripts/build_dim_airport.py",
    "scripts/build_dim_route.py",
    "scripts/audit_dimensions.py"
]

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def safe_child(base, relative):
    rel = Path(relative)

    if rel.is_absolute() or ".." in rel.parts:
        raise RuntimeError(f"Unsafe package path: {relative}")

    resolved = (base / rel).resolve()

    if not resolved.is_relative_to(base.resolve()):
        raise RuntimeError(f"Package path escapes its root: {relative}")

    return resolved

def write_result(path, result):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def restore_snapshot(snapshot_root, token):
    errors = []

    for relative in TARGET_ORDER:
        try:
            source = safe_child(snapshot_root, relative)
            target = safe_child(ROOT, relative)

            if not source.exists():
                raise FileNotFoundError(source)

            temporary = target.with_name(
                target.name + "." + token + ".rollback.tmp"
            )

            shutil.copy2(source, temporary)

            if sha256(temporary) != sha256(source):
                raise RuntimeError(
                    f"Rollback temporary verification failed: {relative}"
                )

            os.replace(temporary, target)

            if sha256(target) != sha256(source):
                raise RuntimeError(
                    f"Rollback verification failed: {relative}"
                )

        except Exception as exc:
            errors.append({
                "destination": relative,
                "error": str(exc)
            })

    return errors

def main():
    if not PACKAGE.exists():
        raise FileNotFoundError(PACKAGE)

    inventory_path = PACKAGE / "DEPLOYMENT_PACKAGE_MANIFEST.json"

    if not inventory_path.exists():
        raise FileNotFoundError(inventory_path)

    inventory = json.loads(
        inventory_path.read_text(encoding="utf-8")
    )

    if inventory.get("status") != "PREPARED_NOT_PROMOTED":
        raise RuntimeError("Release package is not in its prepared state.")

    if inventory.get("promotion_executed") is not False:
        raise RuntimeError("Release inventory indicates prior promotion.")

    deployment = inventory.get("deployment_artifacts", [])
    rollback = inventory.get("rollback_artifacts", [])

    deployment_by_target = {
        item["destination"]: item for item in deployment
    }
    rollback_by_target = {
        item["destination"]: item for item in rollback
    }

    if len(deployment_by_target) != 9 or len(rollback_by_target) != 9:
        raise RuntimeError("Expected exactly nine deployment and rollback entries.")

    if set(deployment_by_target) != EXPECTED_TARGETS:
        raise RuntimeError("Deployment target list differs from approved scope.")

    if set(rollback_by_target) != EXPECTED_TARGETS:
        raise RuntimeError("Rollback target list differs from approved scope.")

    registry = ROOT / "data/04_reference/DIM_ROUTE_KEYMAP_V1.csv"
    registry_hash = sha256(registry)

    if (
        inventory.get("deployment_scope", {})
        .get("route_key_registry_sha256") != registry_hash
    ):
        raise RuntimeError("Permanent route-key registry hash mismatch.")

    print("\n===== 1. VERIFY DEPLOYMENT AND ROLLBACK FILES =====")

    payloads = {}
    snapshots = {}

    for relative in TARGET_ORDER:
        dep = deployment_by_target[relative]
        rb = rollback_by_target[relative]

        payload = safe_child(PACKAGE, dep["payload_path"])
        rollback_file = safe_child(PACKAGE, rb["rollback_path"])
        target = safe_child(ROOT, relative)

        if not payload.exists() or not rollback_file.exists():
            raise FileNotFoundError(relative)

        if sha256(payload) != dep["payload_sha256"]:
            raise RuntimeError(f"Deployment payload hash mismatch: {relative}")

        if sha256(rollback_file) != rb["rollback_sha256"]:
            raise RuntimeError(f"Rollback package hash mismatch: {relative}")

        if not target.exists():
            raise FileNotFoundError(target)

        if sha256(target) != rb["rollback_sha256"]:
            raise RuntimeError(
                f"Production changed since preflight: {relative}"
            )

        if payload.suffix == ".py":
            import ast
            ast.parse(payload.read_text(encoding="utf-8-sig"))

        payloads[relative] = payload
        snapshots[relative] = target

        print("PASS:", relative)
        print("  DEPLOYMENT:", sha256(payload))
        print("  CURRENT PRODUCTION:", sha256(target))

    print("\n===== 2. CREATE IMMEDIATE PRE-PROMOTION SNAPSHOT =====")

    token = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    execution_root = EXECUTIONS / token

    snapshot_root = execution_root / "pre_promotion_snapshot"

    if execution_root.exists():
        raise FileExistsError(execution_root)

    snapshot_root.mkdir(parents=True)

    for relative, target in snapshots.items():
        destination = safe_child(snapshot_root, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(target, destination)

        if sha256(destination) != sha256(target):
            raise RuntimeError(
                f"Immediate snapshot verification failed: {relative}"
            )

    snapshot_hashes = {
        relative: sha256(safe_child(snapshot_root, relative))
        for relative in TARGET_ORDER
    }

    print("SNAPSHOT FILES:", len(snapshot_hashes))
    print("SNAPSHOT VERIFICATION: PASS")

    print("\n===== 3. PREPARE ATOMIC REPLACEMENT FILES =====")

    temporary_files = {}

    try:
        for relative in TARGET_ORDER:
            target = safe_child(ROOT, relative)
            payload = payloads[relative]

            temporary = target.with_name(
                target.name + "." + token + ".promotion.tmp"
            )

            if temporary.exists():
                raise FileExistsError(temporary)

            shutil.copy2(payload, temporary)

            if sha256(temporary) != sha256(payload):
                raise RuntimeError(
                    f"Temporary deployment copy failed: {relative}"
                )

            temporary_files[relative] = temporary

        print("TEMPORARY FILES VERIFIED:", len(temporary_files))

    except Exception:
        for path in temporary_files.values():
            path.unlink(missing_ok=True)
        raise

    print("\n===== 4. COMMIT PRODUCTION RELEASE =====")

    promotion_started = False

    try:
        promotion_started = True

        for relative in TARGET_ORDER:
            target = safe_child(ROOT, relative)
            temporary = temporary_files[relative]

            os.replace(temporary, target)

            expected = deployment_by_target[relative]["payload_sha256"]

            if sha256(target) != expected:
                raise RuntimeError(
                    f"Post-replacement hash mismatch: {relative}"
                )

            print("PROMOTED:", relative)

        print("\nALL NINE PRODUCTION FILES REPLACED AND HASH VERIFIED.")

        print("\n===== 5. RUN PRODUCTION CONSOLIDATED AUDIT =====")

        audit_script = ROOT / "scripts/audit_dimensions.py"
        report_dir = ROOT / "reports/production_expansion_audit"

        report_dir.mkdir(parents=True, exist_ok=True)

        reports_before = set(
            report_dir.glob("DIMENSIONS_CONSOLIDATED_AUDIT_*.json")
        )

        process = subprocess.run(
            [sys.executable, str(audit_script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        print("\n----- AUDITOR OUTPUT -----")
        print(process.stdout)

        if process.stderr:
            print("AUDITOR STDERR:")
            print(process.stderr)

        if process.returncode != 0:
            raise RuntimeError(
                f"Production auditor process exited with {process.returncode}."
            )

        reports_after = set(
            report_dir.glob("DIMENSIONS_CONSOLIDATED_AUDIT_*.json")
        )

        new_reports = reports_after - reports_before

        if len(new_reports) != 1:
            raise RuntimeError(
                f"Expected one new production audit report; "
                f"found {len(new_reports)}."
            )

        audit_path = next(iter(new_reports))

        audit = json.loads(
            audit_path.read_text(encoding="utf-8")
        )

        audit_status = audit.get("status")
        checks_failed = int(audit.get("checks_failed", -1))
        dimensions_expected = int(audit.get("dimensions_expected", -1))
        dimensions_loaded = int(audit.get("dimensions_loaded", -1))

        if checks_failed != 0:
            raise RuntimeError(
                f"Production audit has {checks_failed} failed checks."
            )

        if audit_status not in {"PASS", "PASS_WITH_OPEN_ITEMS"}:
            raise RuntimeError(
                f"Unexpected production audit status: {audit_status}"
            )

        if dimensions_expected != 11 or dimensions_loaded != 11:
            raise RuntimeError(
                "Production audit did not load all 11 dimensions."
            )

        print("PRODUCTION AUDIT STATUS:", audit_status)
        print("CHECKS PASSED:", audit.get("checks_passed"))
        print("CHECKS FAILED:", checks_failed)
        print("DIMENSIONS LOADED:", dimensions_loaded, "/", dimensions_expected)
        print("AUDIT REPORT:", audit_path)

        for relative in TARGET_ORDER:
            target = safe_child(ROOT, relative)
            expected = deployment_by_target[relative]["payload_sha256"]

            if sha256(target) != expected:
                raise RuntimeError(
                    f"Final production hash verification failed: {relative}"
                )

        result = {
            "project": "AEROVISION 360",
            "release": "NETWORK_EXPANSION_V2",
            "status": "PROMOTED_AND_AUDITED",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "production_files_promoted": 9,
            "production_hashes_verified": True,
            "production_audit": {
                "status": audit_status,
                "checks_passed": audit.get("checks_passed"),
                "checks_failed": checks_failed,
                "dimensions_expected": dimensions_expected,
                "dimensions_loaded": dimensions_loaded,
                "report": str(audit_path.relative_to(ROOT))
            },
            "rollback_snapshot": str(snapshot_root.relative_to(ROOT)),
            "rollback_snapshot_hashes": snapshot_hashes,
            "route_key_registry_sha256": registry_hash,
            "disclosure": audit.get("disclosure")
        }

        result_path = execution_root / "PROMOTION_RESULT.json"
        write_result(result_path, result)

        print("\n===== PRODUCTION PROMOTION COMPLETE =====")
        print("STATUS: PROMOTED_AND_AUDITED")
        print("PRODUCTION FILES:", len(TARGET_ORDER))
        print("ROLLBACK SNAPSHOT:", snapshot_root)
        print("PROMOTION RESULT:", result_path)
        print("PRODUCTION AUDIT:", audit_status)
        print("PRODUCTION AUDIT FAILURES:", checks_failed)

    except Exception as exc:
        print("\n===== PROMOTION FAILURE =====")
        print("ERROR:", str(exc))

        rollback_errors = []

        if promotion_started:
            print("AUTOMATIC ROLLBACK STARTED.")
            rollback_errors = restore_snapshot(snapshot_root, token)

        for temporary in temporary_files.values():
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass

        rollback_complete = promotion_started and not rollback_errors

        result = {
            "project": "AEROVISION 360",
            "release": "NETWORK_EXPANSION_V2",
            "status": (
                "ROLLED_BACK_AFTER_FAILURE"
                if rollback_complete
                else (
                    "ROLLBACK_INCOMPLETE"
                    if promotion_started
                    else "FAILED_BEFORE_PRODUCTION_CHANGE"
                )
            ),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "error": str(exc),
            "rollback_complete": rollback_complete,
            "rollback_errors": rollback_errors,
            "rollback_snapshot": str(snapshot_root.relative_to(ROOT))
        }

        result_path = execution_root / "PROMOTION_RESULT.json"
        write_result(result_path, result)

        print("ROLLBACK COMPLETE:", rollback_complete)
        print("PROMOTION RESULT:", result_path)

        if rollback_errors:
            print("CRITICAL: Manual recovery review required.")
            for error in rollback_errors:
                print(error)

        sys.exit(1)

if __name__ == "__main__":
    main()
