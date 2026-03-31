# Reproducible CI/CD with Nix Flakes

Date: 2026-07-01
Mood/Energy: Hopeful and a bit relieved
Estimated reading time: 7 minutes

## The "Why"
I am tired of builds that succeed in one environment and fail in another for reasons that are just vague enough to waste an entire afternoon. Nix Flakes looked like a way to make the environment part of the repository instead of a hidden assumption.

## The Exploration
What I like about Nix is that it makes the whole build environment feel like code. Instead of installing a bunch of tools manually and hoping the CI runner matches my laptop, I define the inputs declaratively and let the flake resolve them the same way everywhere.

My mental picture was:

```text
flake.lock -> exact inputs
flake.nix  -> exact build environment
CI runner  -> just executes it
```

That made reproducibility feel less like a promise and more like a contract.

## The Code (Crucial)
The longer Nix example lives in [code/12_nix_cicd-example.nix](../code/12_nix_cicd-example.nix).

```nix
{
  outputs = { self, nixpkgs }: {
    devShells.x86_64-linux.default = import nixpkgs {
      system = "x86_64-linux";
    }.mkShell {
      buildInputs = [
        nixpkgs.legacyPackages.x86_64-linux.git
        nixpkgs.legacyPackages.x86_64-linux.python3
      ];
    };
  };
}
```

## The "Aha!" Moment
The thing that clicked was that the environment itself becomes versioned. I am not just pinning my dependencies. I am pinning the whole shape of the build.

## The Struggle
I kept treating Nix like a package manager with extra steps, which made it feel obscure instead of useful. The switch happened when I stopped thinking in terms of "install this tool" and started thinking in terms of "describe the exact environment I want." That was a much better fit for CI.

## Key Takeaways
- Flakes make environments reproducible and explicit.
- The lock file matters because it pins the inputs.
- CI gets simpler when the build environment is defined in code.
- Nix feels strange until the declarative model clicks.
- Reproducibility is really about removing hidden state.

## Questions I still have
- What is the cleanest way to scale Nix-based CI for multiple languages?
- How do teams manage Nix adoption without making the workflow too steep for newcomers?
