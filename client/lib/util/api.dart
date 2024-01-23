import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:crypto/crypto.dart';

class Api {
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

  Future<Response> getVideo(String? rul, String? resolution,
      {String? format}) async {
    Map<String, dynamic> body = {
      "url": rul,
      "resolution": resolution,
    };

    if (format != null) {
      body["format"] = format;
    }

    try {
      return await _dio.post(
        "$_baseUrl/download/video",
        options: Options(headers: header),
        data: body,
      );
    } on DioException {
      return Future(
          () => Response(requestOptions: RequestOptions(), statusCode: 404));
    }
  }

  Future<Response> getAudio(
    String? url,
    String? bitrate,
  ) async {
    try {
      return await _dio.post("$_baseUrl/download/audio",
          options: Options(headers: header),
          data: {
            "url": url,
            "resolution": bitrate,
          });
    } on DioException {
      return Future(
          () => Response(requestOptions: RequestOptions(), statusCode: 404));
    }
  }

  Future<dynamic> search(String searchParam) async {
    try {
      Response response = await _dio.post(
        "$_baseUrl/search",
        options: Options(headers: header),
        data: {"keyword": searchParam},
      );

      if (response.statusCode == 200) {
        return response.data["results"];
      } else {
        return List.from([]);
      }
    } on DioException {
      return List.from([]);
    }
  }

  Future<dynamic> getQualities(String? url) async {
    var response = await _dio.post("$_baseUrl/search/qualities",
        options: Options(headers: header),
        data: {
          "url": url,
        });

    if (response.statusCode == 200) {
      return response.data;
    }

    return null;
  }

  Future<dynamic> getImage(String url) async {
    try {
      var response = await _dio.get(
        url,
        options: Options(headers: header, responseType: ResponseType.bytes),
      );

      if (response.statusCode == 200) {
        return response.data;
      }
    } catch (error) {
      return null;
    }

    return null;
  }
}
