# ADD CODE HERE
import json
import sys


def fail(message):
    print("FAIL")
    print(message)
    sys.exit(1)


def only_git_commit_hash_changed(before_tags, after_tags):
    before_tags = before_tags or {}
    after_tags = after_tags or {}

    all_tag_keys = set(before_tags.keys()) | set(after_tags.keys())

    changed_tags = []

    for key in all_tag_keys:
        if before_tags.get(key) != after_tags.get(key):
            changed_tags.append(key)

    return changed_tags == ["GitCommitHash"] or changed_tags == []


def only_tags_changed(before, after):
    before = before or {}
    after = after or {}

    all_keys = set(before.keys()) | set(after.keys())

    for key in all_keys:
        if key == "tags":
            continue

        if before.get(key) != after.get(key):
            return False

    return True


if len(sys.argv) != 2:
    fail("Usage: python script.py <tfplan-json-file>")

file_path = sys.argv[1]

with open(file_path, "r") as f:
    plan = json.load(f)

resource_changes = plan.get("resource_changes", [])

for resource in resource_changes:
    address = resource.get("address", "unknown-resource")
    change = resource.get("change", {})
    actions = change.get("actions", [])

    if actions == ["no-op"]:
        continue

    if actions == ["create"]:
        continue

    if "delete" in actions or "destroy" in actions:
        fail(f"{address} contains forbidden action: {actions}")

    if actions == ["update"]:
        before = change.get("before", {})
        after = change.get("after", {})

        if not only_tags_changed(before, after):
            fail(f"{address} modifies something other than tags")

        before_tags = before.get("tags", {})
        after_tags = after.get("tags", {})

        if not only_git_commit_hash_changed(before_tags, after_tags):
            fail(f"{address} modifies tags other than GitCommitHash")

        continue

    fail(f"{address} contains unsupported action: {actions}")

print("PASS")
print("Terraform plan is safe to apply")

# change script to whatever language you are comfortable with