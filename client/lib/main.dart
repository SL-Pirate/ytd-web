import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:ytd_web/screens/home.dart';
import 'package:permission_handler/permission_handler.dart';

import 'screens/base_frame.dart';

String product = "";

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  MediaKit.ensureInitialized();
  requestStoragePerms();

  if (kIsWeb) {
    product = "YTD-Web";
  }
  else if (Platform.isAndroid || Platform.isIOS) {
    product = "YTD-Mobile";
  }
  else if (Platform.isLinux || Platform.isWindows || Platform.isMacOS) {
    product = "YTD-Desktop";
  }
  else {
    product = "YTDL";
  }

  runApp(const MyApp());
}

void requestStoragePerms() async {
  if (!kIsWeb && Platform.isAndroid) {
    PermissionStatus status = await Permission.storage.status;
    if (status.isDenied) {
      status = await Permission.storage.request();
    }
  }
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'YTD-Web',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: BaseFrame(
        product: product,
        child: const HomePage(),
      )
    );
  }
}
