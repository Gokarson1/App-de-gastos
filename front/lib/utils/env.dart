abstract class EnvConfig {
  static String baseurl = const String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'http://192.168.56.1:8000',
  );
}
