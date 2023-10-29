import 'dart:convert';
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:http/http.dart' as http;
import 'package:crypto/crypto.dart';

class Api{
  static final Api instance = Api._();
  final Dio _dio = Dio();
  final String _baseUrl = const String.fromEnvironment("baseUrl");
  final String _token = const String.fromEnvironment("token");

  Api._();

  Map<String, String> get header {
    String time = DateTime.now().millisecondsSinceEpoch.toString();
    return {
      'Timestamp': time,
      'Token': md5.convert(utf8.encode("$time$_token")).toString()
    };
  }

  Future<Response> getVideo (String videoId, String? resolution) async {
    try{
      return await _dio.get(
          "$_baseUrl/download/video",
          options: Options(
            headers: header
          ),
          queryParameters: {
            "video_id": videoId,
            "resolution": resolution ?? "360p"
          }
      );
    }
    on DioException {
      return Future(() => Response(
          requestOptions: RequestOptions(),
          statusCode: 404
      ));
    }
  }

  Future<dynamic> search(String searchParam) async {
    try{
      Response response = await _dio.get(
          "$_baseUrl/search",
          options: Options(
              headers: header
          ),
          queryParameters: {
            "keyword": searchParam
          }
      );

      return response.data;
    }
    on DioException {
      return Future(() => null);
    }
  }

  Future<Stream<Uint8List>?> getDownloadable(String url) async {
    try {
      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        return Stream.value(response.bodyBytes);

      }
    } catch (error) {
      return null;
    }

    return null;
  }

  Future<dynamic> getQualities(String videoId) async {
    var response = await _dio.get(
        "$_baseUrl/search/qualities",
        options: Options(
            headers: header
        ),
        queryParameters: {
          "video_id": videoId
        }
    );

    if (response.statusCode == 200) {
      return response.data;
    }


    return null;
  }
}
