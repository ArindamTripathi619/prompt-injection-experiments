# Attack Taxonomy

This project tests against a broad spectrum of prompt injection categories based on the latest adversarial research.

```mermaid
mindmap
  root((<span style="color:white">Prompt Injection</span>))
    <span style="color:white">Direct Attacks</span>
      <span style="color:white">Ignore Previous Commands</span>
      <span style="color:white">Reveal System Prompt</span>
      <span style="color:white">System Override</span>
    <span style="color:white">Semantic Attacks</span>
      <span style="color:white">Polite Inquiries</span>
      <span style="color:white">Researcher Emulation</span>
      <span style="color:white">Debugging Context</span>
    <span style="color:white">Context Override</span>
      <span style="color:white">Role Impersonation</span>
      <span style="color:white">XML-Tag Injection</span>
      <span style="color:white">Delimiter Hijacking</span>
    <span style="color:white">Encoding Attacks</span>
      <span style="color:white">Base64 Obfuscation</span>
      <span style="color:white">ROT13 Payload</span>
      <span style="color:white">Unicode Escaping</span>
    <span style="color:white">Jailbreak Styles</span>
      <span style="color:white">DAN Mode</span>
      <span style="color:white">Alternate Universe</span>
      <span style="color:white">Simulation Games</span>
    <span style="color:white">Stealth Attacks</span>
      <span style="color:white">Data Leakage</span>
      <span style="color:white">Indirect Injection</span>
      <span style="color:white">Prefix Injection</span>
```

## Evaluated Categories

- **Direct Injection**: Classic "Ignore all previous instructions" style attacks.
- **Semantic Injection**: Sophisticated social engineering prompts that appear benign to keyword filters.
- **Context Override**: Attempts to use role-based messages or tags to trick the model into a system role.
- **Encodings**: Using Base64 or other encodings to bypass preliminary classification layers.
- **Stealth**: High-complexity attacks designed to exploit Trust Boundary violations even in isolated environments.
