# Target Architectures

`target-arch` is a required argument, and defines the architecture of
the resulting kernel. It may be one of the following:

- `arc`
- `arm`
- `arm64`
- `hexagon`
- `i386`
- `mips`
- `parisc`
- `powerpc`
- `riscv`
- `s390`
- `sh`
- `sparc`
- `x86_64`

Each architecture will be built from an x86_64 host.

## Examples

### `tuxsuite build`

Perform a powerpc tinyconfig build against mainline using the most recent
nightly version of Clang.

```sh
tuxsuite build \
--git-repo 'https://github.com/torvalds/linux.git' \
--git-ref master \
--target-arch powerpc \
--toolchain clang-nightly \
--kconfig tinyconfig
```
