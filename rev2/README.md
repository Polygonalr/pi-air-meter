# Air Quality Dashboard for Raspberry Pi (Revision 2)

## Wire connection

// TO ADD LATER

## Usage

```
./dashboard
```

## Cross-Compilation from Ubuntu 22.04

Directly compiling for Raspberry Pi OS `bullseye` (which is the latest version of Raspberry Pi OS as of writing this) is currently not supported due to the version of the `libc` linker on the Ubuntu machine being too new - `bullseye` by default does not have the newer `libc` versions. Therefore, it is a requirement to compile for the target `aarch64-unknown-linux-musl` to use static linking. `clang` is used instead of `gcc` due to `gcc` having some issues.

Install the required tools with the following command. 

```
sudo apt-get install musl-tools clang llvm -y
```

To tell `cargo` to use `clang` as the linker, export the following environment values.

```
export CC_aarch64_unknown_linux_musl=clang
export AR_aarch64_unknown_linux_musl=llvm-ar
export CARGO_TARGET_AARCH64_UNKNOWN_LINUX_MUSL_RUSTFLAGS="-Clink-self-contained=yes -Clinker=rust-lld"
```

Finally, compile the project with the following command.

```
cargo build --release --target aarch64-unknown-linux-musl
```

The compiled program can be found at `target/aarch64-unknown-linux-musl/release` and can be transferred over to a Raspberry Pi to be executed.
