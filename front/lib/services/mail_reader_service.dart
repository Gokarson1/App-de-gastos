import 'package:http/http.dart' as http;
import 'dart:convert';
import '../utils/env.dart';

class MailReaderService {
  final String baseUrl = EnvConfig.baseurl;

  Future<bool> sendGoogleAccessToken(String accessToken) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/analizar-correos'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'access_token': accessToken}),
      );

      if (response.statusCode == 200) {
        return true;
      } else {
        print('Error: ${response.statusCode}');
        print('Response: ${response.body}');
        return false;
      }
    } catch (e) {
      print('Exception when sending access token: $e');
      return false;
    }
  }
}
