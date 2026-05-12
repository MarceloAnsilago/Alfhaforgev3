## Theme presets

O frontend do `V3` agora usa presets de tema para facilitar rollback visual.

- Preset atual: `v2_classic`
- Preset anterior preservado: `modern_legacy`

Arquivo de troca:

- [theme.py](/C:/Users/User/AppData/Roaming/MetaQuotes/Terminal/FB9A56D617EDDDFE29EE54EBEFFE96C1/MQL5/Experts/Advisors/V3/Frontend/themes/theme.py:1)

Para voltar ao visual anterior, altere:

```python
DEFAULT_THEME_PRESET = "modern_legacy"
```

Para usar o visual inspirado no `V2`:

```python
DEFAULT_THEME_PRESET = "v2_classic"
```
