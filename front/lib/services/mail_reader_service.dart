import 'package:dio/dio.dart';
import '../utils/env.dart';

class MailReaderService {
  final Dio dio = Dio();

  final String baseUrl = EnvConfig.baseurl;

  Future<bool> sendGoogleAccessToken(String accessToken) async {
    try {
      final response = await dio.post(
        'http://$baseUrl:8000/analizar-correos',
        data: {'access_token': accessToken},
        options: Options(headers: {'Content-Type': 'application/json'}),
      );

      print('Respuesta del backend: ${response.data}');
      return true;
    } catch (e) {
      print('Error al enviar token: $e');
      return false;
    }
  }
}
