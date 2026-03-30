# Attack Taxonomy

This project tests against a broad spectrum of prompt injection categories based on the latest adversarial research.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'mindmapTextColor': '#fff', 'mindmapNodeTextColor': '#fff' }}}%%
mindmap
  root((Prompt Injection))
    Direct Attacks
      Ignore Previous Commands
      Reveal System Prompt
      System Override
    Semantic Attacks
      Polite Inquiries
      Researcher Emulation
      Debugging Context
    Context Override
      Role Impersonation
      XML-Tag Injection
      Delimiter Hijacking
    Encoding Attacks
      Base64 Obfuscation
      ROT13 Payload
      Unicode Escaping
    Jailbreak Styles
      DAN Mode
      Alternate Universe
      Simulation Games
    Stealth Attacks
      Data Leakage
      Indirect Injection
      Prefix Injection
```

## Evaluated Categories

- **Direct Injection**: Classic "Ignore all previous instructions" style attacks.
- **Semantic Injection**: Sophisticated social engineering prompts that appear benign to keyword filters.
- **Context Override**: Attempts to use role-based messages or tags to trick the model into a system role.
- **Encodings**: Using Base64 or other encodings to bypass preliminary classification layers.
- **Stealth**: High-complexity attacks designed to exploit Trust Boundary violations even in isolated environments.
