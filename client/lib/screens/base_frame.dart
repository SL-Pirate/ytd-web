import 'package:flutter/material.dart';
import 'package:ytd_web/util/styles.dart';

class BaseFrame extends StatelessWidget {
  final Widget child;
  final String product;

  const BaseFrame({
    super.key,
    required this.child,
    required this.product
  });

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: PreferredSize(
          preferredSize: const Size(double.infinity, 250),
          child: Material(
            color: Styles.blue,
            child: Material(
              elevation: 10,
              color: Styles.blue,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: Image.asset(
                        "assets/img/logo.png",
                        width: 100,
                        height: 50
                    ),
                  ),
                  Container(
                    width: 90,
                    height: 35,
                    margin: const EdgeInsets.all(20),
                    decoration: const BoxDecoration(
                        color: Styles.red,
                        borderRadius: BorderRadius.all(Radius.circular(5))
                    ),
                    child: TextButton(
                      onPressed: () {},
                      child: const Text(
                        "Log In",
                        style: TextStyle(
                            color: Styles.white,
                            fontSize: 12,
                            fontFamily: Styles.fontFamily,
                            fontWeight: FontWeight.bold
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),
          ),
        ),
        body: Material(
          color: Styles.blue,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const SizedBox(),
              child,
              Container(
                width: double.infinity,
                height: 30,
                color: Styles.black.withOpacity(0.25),
                child: Center(
                  child: Text(
                    "Copyright © ${DateTime.now().year} $product. "
                        "All Rights Reserved",
                    style: TextStyle(
                        color: Styles.grey.withOpacity(0.5),
                        fontSize: 12,
                        fontFamily: Styles.fontFamily
                    ),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}