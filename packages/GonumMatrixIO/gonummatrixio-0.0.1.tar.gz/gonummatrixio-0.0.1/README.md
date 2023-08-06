# gonum-matrix-io
Offers some utilities to save [Gonum](https://pkg.go.dev/gonum.org/v1/gonum) matrices and vectors to a binary file, as well as some python scripts to load these files into numpy

## Usage

For use in Go, run `go get -u github.com/hmcalister/gonum-matrix-io`.

You may then import `hmcalister/gonum-matrix-io/gonumio` in your Go code, and use `gonumio.SaveMatrix` to save a matrix (for example).

---

On the Python side, copy the script `Python/GonumIO.py` to your project. `import * from GonumIO` will then allow usage of `loadMatrix()` for example.