# Zmiany — polskie znaki i NIE WIEM

1. `configs/config_ux_ab_demo.yaml`
   - instrukcje zapisane jako ASCII + sekwencje YAML Unicode;
   - po `yaml.safe_load()` tekst ma poprawne polskie znaki.

2. `examples/ux_ab_demo/apply_demo_source_patch.py`
   - ustawia `encoding="utf-8"` w `CustomConfig.read_config()`;
   - zmienia `TextDataset` z `none` na `nie wiem`.

3. `examples/ux_ab_demo/tobii_pytracker_demo_fixes.patch`
   - ta sama poprawka w formacie `git diff`, do ręcznego użycia przez `git apply`.
