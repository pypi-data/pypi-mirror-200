#include <vector>

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

namespace nb = nanobind;

using namespace nb::literals;

auto histogram(nb::ndarray<double, nb::shape<nb::any>> x,
               int64_t nbins,
               double xmin,
               double xmax) {
  int64_t* c = new int64_t[nbins];
  std::memset(c, 0, sizeof(int64_t) * nbins);
  size_t shape[1] = {static_cast<size_t>(nbins)};
  nb::capsule owner(c, [](void *p) noexcept { delete [] (int64_t*) p; });
  double norm = static_cast<double>(nbins) / (xmax - xmin);
  size_t bin;
  double v;
  for (size_t i = 0; i < x.shape(0); ++i) {
    v = x(i);
    if (v<xmin) continue;
    if (v>=xmax) continue;
    bin = static_cast<size_t>((v - xmin) * norm);
    c[bin] += 1;
  }

  return nb::ndarray<nb::numpy, int64_t>(c, 1, shape, owner);
}

NB_MODULE(_backend, m) {
  m.def("hist", &histogram, "x"_a, "nbins"_a, "xmin"_a, "xmax"_a);
}
