import 'package:flutter/material.dart';
import 'package:html_unescape/html_unescape.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/models/search_result_model.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/components/channel_label.dart';

class SearchResultComponent extends StatelessWidget {
  final SearchResultModel searchResultModel;
  const SearchResultComponent(this.searchResultModel, {super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        FutureBuilder(
            future: searchResultModel.getThumbnail(
              width: Styles.of(context).isMobile ? 186 : 444,
              height: Styles.of(context).isMobile ? 109 : 241,
              fit: BoxFit.fitWidth,
            ),
            builder: (context, snapshot) {
              if (!snapshot.hasData) {
                return Container(
                  color: Colors.black,
                  child: const Center(child: CircularProgressIndicator()),
                );
              }

              return snapshot.data!;
            }),
        SizedBox(width: Styles.of(context).isMobile ? 10 : 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(HtmlUnescape().convert(searchResultModel.title),
                  style: TextStyle(
                      fontSize: Styles.of(context).subtitleFontSize,
                      fontWeight: FontWeight.bold,
                      color: Styles.textColor,
                      fontFamily: Styles.fontFamily)),
              SizedBox(
                height: Styles.of(context).isMobile ? 15 : 20,
              ),
              ChannelLabel(searchResultModel: searchResultModel)
            ],
          ),
        )
      ],
    );
  }
}

dynamic child = Card(
  child: Column(
    children: [
      const Text("searchResultModel.title"),
      FutureBuilder(
          future: Api.instance.getImage("searchResultModel.thumbnailUrl"),
          builder: (context, snapshot) {
            if (!snapshot.hasData) {
              return const Center(child: CircularProgressIndicator());
            }

            return Image.memory(snapshot.data);
          }),
      const Text("searchResultModel.channelName")
    ],
  ),
);
