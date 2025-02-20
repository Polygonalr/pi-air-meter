# Air Quality Dashboard for Raspberry Pi (Revision 2)

## Requirement

- Raspberry Pi OS that is at least `bookworm` (`bullseye` and older versions not supported).

## Wire connection

// TO ADD LATER

## Usage

```
./dashboard
```

## Cross-Compilation from Ubuntu 22.04

Install the required rustup toolchain with the following command.

```
rustup toolchain install stable-aarch64-unknown-linux-gnu --force-non-host
```

Finally, compile the project with the following command.

```
cargo build --release --target aarch64-unknown-linux-gnu
```

The compiled program can be found at `target/aarch64-unknown-linux-gnu/release` and can be transferred over to a Raspberry Pi to be executed.
