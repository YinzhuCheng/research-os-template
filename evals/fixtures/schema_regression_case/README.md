# Schema Regression Fixture

This fixture exists to ensure strict validation catches:

- unquoted YAML dates where schemas require strings;
- `null` placeholders where schemas require strings;
- registry wrapper files validated with the registry schema;
- content after the final `</html>` tag.
