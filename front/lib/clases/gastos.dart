class Gastos {
  final String gasto;
  final String moneda;
  final String tipo_gasto;

  Gastos({required this.gasto, required this.moneda, required this.tipo_gasto});

  factory Gastos.fromJson(Map<String, dynamic> json) {
    return Gastos(
      gasto: json['gasto'] ?? '',
      moneda: json['moneda'] ?? '',
      tipo_gasto: json['tipo_gasto'] ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    'gasto': gasto,
    'moneda': moneda,
    'tipo_gasto': tipo_gasto,
  };
}
