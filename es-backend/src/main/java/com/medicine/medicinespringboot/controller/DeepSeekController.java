///*
// * @Author: Zayy2005x 2781310592@qq.com
// * @Date: 2025-03-08 23:22:15
// * @LastEditors: Zayy2005x 2781310592@qq.com
// * @LastEditTime: 2025-03-14 21:39:36
// * @FilePath: \medicine-SpringBoot\src\main\java\com\medicine\medicinespringboot\controller\DeepSeekController.java
// */
///*
// *                        _oo0oo_
// *                       o8888888o
// *                       88" . "88
// *                       (| -_- |)
// *                       0\  =  /0
// *                     ___/`---'\___
// *                   .' \\|     |// '.
// *                  / \\|||  :  |||// \
// *                 / _||||| -:- |||||- \
// *                |   | \\\  - /// |   |
// *                | \_|  ''\---/''  |_/ |
// *                \  .-\__  '-'  ___/-. /
// *              ___'. .'  /--.--\  `. .'___
// *           ."" '<  `.___\_<|>_/___.' >' "".
// *          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
// *          \  \ `_.   \_ __\ /__ _/   .-` /  /
// *      =====`-.____`.___ \_____/___.-`___.-'=====
// *                        `=---='
// *
// *
// *      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// *
// *            佛祖保佑     永不宕机     永无BUG
// *
// */
//
//package com.medicine.medicinespringboot.controller;
//import com.google.gson.Gson;
//import com.mashape.unirest.http.HttpResponse;
//import com.mashape.unirest.http.Unirest;
//import com.mashape.unirest.http.exceptions.UnirestException;
//import com.medicine.medicinespringboot.pojo.DeepSeekRequest;
//import lombok.extern.slf4j.Slf4j;
////import okhttp3.MediaType;
////import okhttp3.OkHttpClient;
////import okhttp3.Request;
////import okhttp3.RequestBody;
////import okhttp3.Response;
////import org.junit.jupiter.api.Test;
//import org.springframework.beans.factory.annotation.Value;
//import org.springframework.web.bind.annotation.*;
//
//import java.io.IOException;
//import java.util.ArrayList;
//import java.util.Collections;
//import java.util.List;
//
//
//
//@Slf4j
//@RestController
//public class DeepSeekController {
//    private final Gson gson = new Gson();
//
//    @PostMapping("tall")
//    public String tallQuestion(@RequestBody String question) throws IOException, UnirestException {
//
//        Unirest.setTimeouts(0, 0);
//        List<DeepSeekRequest.Message> messages = new ArrayList<>();
//        messages.add(DeepSeekRequest.Message.builder().role("system").content("你是一名专业的癫痫医生，接下来会给你一个癫痫患者的病情情况，你需要向一名医生给出你的会诊意见").build());
//        messages.add(DeepSeekRequest.Message.builder().role("user").content(question).build());
//        DeepSeekRequest requestBody = DeepSeekRequest.builder()
//                .model("deepseek-v3")
//                .messages(messages)
//                .build();
//        HttpResponse<String> response = Unirest.post("https://api.qnaigc.com/v1/chat/completions")
//                .header("Content-Type", "application/json")
//                .header("Accept", "application/json")
//                .header("Authorization", "Bearer "+API_KEY)
//                .body(gson.toJson(requestBody))
//                .asString();
//        return  response.getBody();
//
//    }
//
//
//}
