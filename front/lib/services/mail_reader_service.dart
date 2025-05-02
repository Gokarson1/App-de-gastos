import 'package:dio/dio.dart';
import '../utils/env.dart';
import '../clases/gastos.dart';

class MailReaderService {
  final Dio dio = Dio();

  final String baseUrl = EnvConfig.baseurl;

  Future<List<Gastos>> sendGoogleAccessToken(String accessToken) async {
    try {
      final response = await dio.post(
        'http://192.168.56.1:8000/analizar-correos',
        data: {'access_token': accessToken},
        options: Options(headers: {'Content-Type': 'application/json'}),
      );
      List<dynamic> gastosList = response.data as List<dynamic>;
      return gastosList.map((gastoJson) => Gastos.fromJson(gastoJson)).toList();
    } catch (e) {
      throw Exception('Failed to analyze emails: $e');
    }
  }
}
