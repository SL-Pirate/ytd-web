import 'package:flutter/material.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/util/styles.dart';

class ChannelLabel extends StatelessWidget {
  final SearchResultModel searchResultModel;
  const ChannelLabel({super.key, required this.searchResultModel});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        FutureBuilder(
            future: searchResultModel.channelThumbnailProvider,
            builder: (context, snap) {
              return CircleAvatar(
                radius: Styles.of(context).isMobile ? 12.58 : 15,
                backgroundColor: Styles.white,
                backgroundImage: snap.data,
                child: snap.data == null ? Center(
                    child: Icon(
                      Icons.person,
                      size: Styles.of(context).isMobile ? 12.58 : 15,
                    )
                ) : null,
              );
            }
        ),
        const SizedBox(
          width: 10,
        ),
        Expanded(
          child: Text(
              searchResultModel.channelName,
              style: TextStyle(
                  fontSize: Styles.of(context).fontSizeSmall,
                  fontWeight: FontWeight.bold,
                  color: Styles.white,
                  fontFamily: Styles.fontFamily
              ),
              overflow: TextOverflow.ellipsis
          ),
        ),
      ],
    );
  }
}

