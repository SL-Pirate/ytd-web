import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:ytd_web/components/SearchResultsComponent.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _ctrlr = TextEditingController();
  String? output;
  late String product;

  @override
  void initState() {
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

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: PreferredSize(
          preferredSize: const Size(double.infinity,  125),
          child: Container(
            color: Colors.blue,
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    "Welcome to $product",
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 24
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8.0),
                  child: SearchBar(
                    controller: _ctrlr,
                    trailing: [
                      IconButton(
                          onPressed: () {
                            if (_ctrlr.text.isNotEmpty) {
                              setState(() {
                                output = _ctrlr.text;
                              });
                            }
                          },
                          icon: const Icon(Icons.search)
                      )
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
        body: SearchResultsComponent(output),
      ),
    );
  }
}
