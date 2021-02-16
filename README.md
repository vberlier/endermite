<p align="center">
  <br>
  <img src="docs/assets/logo.svg" alt="logo" width="76">
  <br>
</p>

# Endermite

> A high-level, expressive component system that turns Minecraft into a game engine.

## Introduction

The goal of the `endermite` project is to bring intentional developer experience to Minecraft map-making.

```python
from endermite import Component

class PlayerController(Component):
    def start(self):
        self.log("Hello, world!")
```

---

License - [MIT](https://github.com/vberlier/endermite/blob/main/LICENSE)
