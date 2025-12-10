#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <string>

#if defined(_WIN32)
#include <windows.h>
#endif

// Normal PDF
double normal_pdf(double x) {
    static const double inv_sqrt_2pi = 1.0 / std::sqrt(2.0 * M_PI);
    return inv_sqrt_2pi * std::exp(-0.5 * x * x);
}

// Simpson's rule on [a,b] with n even
double simpson_integrate(double (*f)(double), double a, double b, int n) {
    if (a == b) return 0.0;
    if (n % 2 == 1) ++n;
    double h = (b - a) / n;
    double s = f(a) + f(b);
    for (int i = 1; i < n; ++i) {
        double x = a + i * h;
        s += (i % 2 == 0) ? 2.0 * f(x) : 4.0 * f(x);
    }
    return s * h / 3.0;
}

// Standard normal CDF using Simpson: integrate from 0 to z and use symmetry
double normal_cdf(double z) {
    if (z == 0.0) return 0.5;
    if (z > 0.0) {
        // choose n proportional to |z| for accuracy
        int n = std::max(100, static_cast<int>(std::ceil(200 * std::abs(z))));
        return 0.5 + simpson_integrate(normal_pdf, 0.0, z, n);
    } else {
        return 1.0 - normal_cdf(-z);
    }
}

// Enable ANSI colors on Windows 10+ console
void enable_ansi_if_windows() {
#if defined(_WIN32)
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut == INVALID_HANDLE_VALUE) return;
    DWORD dwMode = 0;
    if (!GetConsoleMode(hOut, &dwMode)) return;
    dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
    SetConsoleMode(hOut, dwMode);
#endif
}

int main() {
    enable_ansi_if_windows();

    std::cout << std::fixed << std::setprecision(4);

    double z_input;
    std::cout << "Ingresa el valor Z (puede ser negativo): ";
    if (!(std::cin >> z_input)) {
        std::cerr << "Entrada invalida.\n";
        return 1;
    }

    // Compute CDF for the input
    double cdf_input = normal_cdf(z_input);
    std::cout << "\nCDF para Z = " << z_input << "  =>  " << cdf_input << "\n\n";

    // Build table values for z from 0.00 to 3.09 (rows 0.0..3.0 step 0.1, cols 0.00..0.09)
    const double z_max = 3.09;
    const int rows = 31; // 0.0 .. 3.0 inclusive -> 31 rows (0.0,0.1,...,3.0)
    const int cols = 10; // 0.00 .. 0.09
    std::vector<std::vector<double>> table(rows, std::vector<double>(cols, 0.0));

    for (int r = 0; r < rows; ++r) {
        double row_base = 0.0 + 0.1 * r;
        for (int c = 0; c < cols; ++c) {
            double z = row_base + 0.01 * c;
            if (z > z_max) table[r][c] = NAN;
            else table[r][c] = normal_cdf(z);
        }
    }

    // Determine which cell corresponds to the absolute value of the input (Z-tables usually show non-negative z)
    double z_abs = std::abs(z_input);
    if (z_abs > z_max) {
        std::cout << "Valor Z fuera del rango de la tabla (>" << z_max << ").\n";
    }
    // round to 2 decimals to find table cell
    double z_round = std::round(z_abs * 100.0) / 100.0;
    int highlight_row = static_cast<int>(std::floor(z_round * 10.0 + 1e-9)); // e.g., 1.23 -> floor(12.3) = 12 -> row=1 (0.1)
    int highlight_col = static_cast<int>(std::round((z_round - (highlight_row / 10.0)) * 100.0 + 1e-9)) % 10;

    if (highlight_row < 0) highlight_row = 0;
    if (highlight_row >= rows) highlight_row = rows - 1;
    if (highlight_col < 0) highlight_col = 0;
    if (highlight_col >= cols) highlight_col = cols - 1;

    // Print header
    std::cout << "       ";
    for (int c = 0; c < cols; ++c) {
        std::cout << std::setw(9) << std::setprecision(2) << std::fixed << (0.00 + 0.01 * c);
    }
    std::cout << std::setprecision(4) << std::fixed << "\n";

    // Print rows
    for (int r = 0; r < rows; ++r) {
        double row_label = 0.0 + 0.1 * r;
        std::cout << std::setw(5) << std::setprecision(1) << std::fixed << row_label << " | ";
        for (int c = 0; c < cols; ++c) {
            double val = table[r][c];
            if (std::isnan(val)) {
                std::cout << std::setw(9) << "   -";
                continue;
            }
            // Check if this is the highlighted cell
            bool is_highlight = (r == highlight_row && c == highlight_col && z_abs <= z_max);
            if (is_highlight) {
                // Use ANSI color: reverse video and yellow text
                std::cout << "\x1b[7m" << "\x1b[33m" << std::setw(9) << val << "\x1b[0m";
            } else {
                std::cout << std::setw(9) << val;
            }
        }
        std::cout << "\n";
    }

    // If input was negative, explain symmetry
    if (z_input < 0) {
        std::cout << "\nNota: la tabla muestra valores para Z >= 0. Para Z negativo, CDF(Z) = 1 - CDF(|Z|).\n";
        std::cout << "CDF calculada para Z = " << z_input << " : " << cdf_input << "\n";
    }

    return 0;
}