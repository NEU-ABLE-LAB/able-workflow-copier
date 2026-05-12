---
name: Release Tagged Version
about: Prepare and track a new tagged release
title: 'Release v'
labels: 'release,chore'
assignees: ''
type: Task

---

Use this issue to prepare a new tagged release. Start by reviewing commits since the last tagged release and curating `CHANGELOG.md`.

## Release target

- Proposed version tag: `v`
- Release owner:
- Target date:
- Release type: [ ] patch [ ] minor [ ] major

## Baseline review

- [ ] Identify the last tagged release
- [ ] Review commits in `last_tag..HEAD`
- [ ] Review merged PRs/issues since that tag
- [ ] Note any breaking changes, migrations, or user-visible behavior changes

## Changelog

- [ ] Review commits since the last tagged release before editing `CHANGELOG.md`
- [ ] Move ready entries from `## dev` into a new tagged section
- [ ] Classify entries under `Changed`, `Added`, `Removed`, and `Fixed`
- [ ] Remove stale, duplicate, or unclear entries
- [ ] Add the release date to the new tagged section
- [ ] Recreate the `## dev` section for future work

## Release validation

- [ ] Run targeted tests for the touched areas
- [ ] Run release-critical tox environments
- [ ] Build docs if docs or templates changed
- [ ] Regenerate maintained examples or fixtures if their sources changed
- [ ] Confirm CI and workflow changes are exercised
- [ ] Confirm submodule pointers or parent-template references are up to date

## Multi-level copier release coordination

- [ ] Create or link release issues for each dependent template: `able-workflow-module-copier`, `able-workflow-etl-copier`, `able-workflow-rule-copier`
- [ ] In each child issue, link back to this parent release issue
- [ ] Create or confirm working branches for each child release update
- [ ] After this repo is ready, update each child repo's `able-workflow-copier` submodule to the intended parent release commit
- [ ] Run the relevant child-repo tests after the parent submodule update to confirm they still pass with the new parent
- [ ] Open and merge the child PRs needed to carry the parent submodule update
- [ ] Prepare and tag the coordinated child releases after their validations pass

## Tagging and publishing

- [ ] Confirm the release version and tag name
- [ ] Confirm `pyproject.toml` versioning is tag-driven via `setuptools_scm` and does not need a manual bump
- [ ] Confirm the release branch or PR is merged, or otherwise ready to tag
- [ ] Create and push an annotated tag
- [ ] Confirm GitHub Actions triggered as expected
- [ ] Verify release artifacts, docs publication, or follow-on automation if applicable

## Post-release follow-up

- [ ] Confirm `CHANGELOG.md` is committed in the released state
- [ ] Open follow-up issues for deferred work
- [ ] Document or announce migration notes if needed

## Notes

- Compare range / link:
- Candidate PRs/issues:
- Child release issues / PRs:
- Risks / rollback notes:
- Follow-up work:
