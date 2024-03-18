import 'package:flutter/material.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:html_unescape/html_unescape.dart';
import 'package:ytd_web/components/channel_label.dart';
import 'package:ytd_web/models/search_result_model.dart';

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
                child: const Center(
                  child: CircularProgressIndicator(),
                ),
              );
            }

            return snapshot.data!;
          },
        ),
        SizedBox(width: Styles.of(context).isMobile ? 10 : 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                HtmlUnescape().convert(searchResultModel.title),
                style: TextStyle(
                  fontSize: Styles.of(context).subtitleFontSize,
                  fontWeight: FontWeight.bold,
                  color: Styles.textColor2,
                  fontFamily: Styles.fontFamily,
                  wordSpacing: Styles.of(context).isMobile ? -2 : 0,
                ),
              ),
              SizedBox(
                height: Styles.of(context).isMobile ? 5 : 10,
              ),
              ChannelLabel(searchResultModel: searchResultModel)
            ],
          ),
        )
      ],
    );
  }
}
