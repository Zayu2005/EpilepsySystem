package com.medicine.medicinespringboot.controller;


import com.medicine.medicinespringboot.pojo.*;
import com.medicine.medicinespringboot.service.Impl.FeatureService;
import com.medicine.medicinespringboot.utils.QiniuUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;
import java.util.UUID;

@RestController
@Slf4j
@RequestMapping("/feature")
public class FeatureController {

    @Autowired
    private QiniuUtil qiniuUtil;

    @Autowired
    private FeatureService featureService;

    @PostMapping("/upload")
    public Result upload(@RequestParam MultipartFile file,
                         @RequestParam("patientId") Integer patientId,
                         @RequestParam("userId") Integer userId
    ) throws IOException {
        System.out.println(file);
        log.info("可视化文件上传：{},病人id{},医生id{}", file.getOriginalFilename(), patientId, userId);
        if (file.isEmpty()) {
            return Result.error("上传文件为空");
        }
        //获取文件名称
        String originalFilename = file.getOriginalFilename();
        //获取后缀名
        String suffix = originalFilename.substring(originalFilename.lastIndexOf("."));
        //为了避免同名覆盖问题,构建新的文件名
        String fileName = UUID.randomUUID().toString() + suffix;
        //调用七牛云OSS工具类
        String url = qiniuUtil.uploadByBytes(file.getBytes(), fileName);
        //查询是否已经上传过该病人的EEG文件
        EegFeaturesFile eegFeaturesFile = featureService.findByPatientIdAndUserId(patientId, userId);
        if (eegFeaturesFile == null) {
            //如果没有上传过,则保存到数据库
            featureService.add(patientId, userId, url);
        } else {
            log.info("可视化文件上传：{},病人id{},医生id{} : 删除原先文件Url", file.getOriginalFilename(), patientId, userId);
            qiniuUtil.deleteFileDirect(eegFeaturesFile.getUrl());
            //如果已经上传过,则更新数据库中的url
            log.info("可视化文件上传：{},病人id{},医生id{} : 更新文件Url", file.getOriginalFilename(), patientId, userId);
            featureService.updateUrl(patientId, userId, url);
        }
        return Result.success("上传成功");
    }


    @GetMapping("/analysis")
    @Transactional
    public Result analysis(@RequestParam("patientId") Integer patientId, @RequestParam("userId") Integer userId) throws IOException, InterruptedException {
        log.info("分析可视化文件：病人id{},医生id{}", patientId, userId);
        EegFeaturesFile eegFeaturesFile = featureService.findByPatientIdAndUserId(patientId, userId);
        if (eegFeaturesFile == null) {
            return Result.error("未上传可视化文件");
        }
        String edfFileUrl  = eegFeaturesFile.getUrl();

        try {
            //构造 Flask 分析接口的完整 URL
            String flaskAnalysisUrl = "http://localhost:5001/feature?url=" + edfFileUrl;
            //创建 RestTemplate 并设置支持 text/plain
            RestTemplate restTemplate = new RestTemplate();
            //发送 GET 请求并接收 JSON 响应
            Map<String, Object> response = restTemplate.getForObject(flaskAnalysisUrl, Map.class);
            //将分析的结果保存到数据库
            return Result.success(response);
        }
        catch (Exception e) {
            return Result.error("调用分析服务失败: " + e.getMessage());
        }
    }
}
