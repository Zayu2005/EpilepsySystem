package com.medicine.medicinespringboot.controller;


import com.aliyuncs.CommonResponse;
import com.medicine.medicinespringboot.pojo.*;
import com.medicine.medicinespringboot.service.Impl.EegService;
import com.medicine.medicinespringboot.service.Impl.UserService;
import com.medicine.medicinespringboot.utils.QiniuUtil;
import com.medicine.medicinespringboot.utils.ThreadLocalUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import static java.lang.Thread.sleep;

@RestController
@Slf4j
@RequestMapping("/eeg")
public class EegController {


    @Autowired
    private UserService userService;
    @Autowired
    private QiniuUtil qiniuUtil;
    @Autowired
    private EegService eegService;

    //上传文件eeg文件
    @PostMapping("/upload")
    public Result upload(@RequestParam MultipartFile file,
                         @RequestParam("patientId") Integer patientId,
                         @RequestParam("userId") Integer userId
    ) throws IOException {
        log.info("文件上传：{},病人id{},医生id{}", file.getOriginalFilename(), patientId, userId);
        if (file.isEmpty()) {
            return Result.error("上传文件为空");
        }
        EegAnalysis eegAnalysis =  eegService.findEegByPatientIdAndUserId(patientId,userId);
        if(eegAnalysis == null){
            log.info("未上传过EEG,进行上传");
            //获取文件名称
            String originalFilename = file.getOriginalFilename();
            //获取后缀名
            String suffix = originalFilename.substring(originalFilename.lastIndexOf("."));
            //为了避免同名覆盖问题,构建新的文件名
            String fileName = UUID.randomUUID().toString() + suffix;
            //调用七牛云OSS工具类
            String url = qiniuUtil.uploadByBytes(file.getBytes(), fileName);
            eegService.add(patientId, userId, url);
        }else{
            log.info("已上传过EEG,进行覆盖");
            //获取文件名称
            String originalFilename = file.getOriginalFilename();
            //获取后缀名
            String suffix = originalFilename.substring(originalFilename.lastIndexOf("."));
            //为了避免同名覆盖问题,构建新的文件名
            String fileName = UUID.randomUUID().toString() + suffix;
            //调用七牛云OSS工具类
            String url = qiniuUtil.uploadByBytes(file.getBytes(), fileName);
            log.info("删除原EEG文件");
            qiniuUtil.deleteFileDirect(eegAnalysis.getUrl());
            eegService.update(patientId, userId, url);
            log.info("覆盖成功");
        }
        return Result.success();
    }

    //分析eeg文件
    @GetMapping("/analysis")
    public Result analysis(@RequestParam("patientId") Integer patientId,@RequestParam("userId") Integer userId) throws IOException, InterruptedException {
        log.info("分析eeg文件：病人id{},医生id{}", patientId, userId);
        EegAnalysis eegAnalysis = eegService.findAnalysisByPatientId(patientId);
        if(eegAnalysis==null){
            return Result.error("未上传eeg文件");
        }
        //获得eeg文件的url地址
        String edfFileUrl = eegAnalysis.getUrl();

        try {
            //构造 Flask 分析接口的完整 URL
            String flaskAnalysisUrl = "http://localhost:5001/analysis?url=" + edfFileUrl;
            //创建 RestTemplate 并设置支持 text/plain
            RestTemplate restTemplate = new RestTemplate();
            //发送 GET 请求并接收 JSON 响应
            Map<String, Object> response = restTemplate.getForObject(flaskAnalysisUrl, Map.class);
            //将分析的结果保存到数据库
            eegService.saveAnalysisResult(response,patientId,userId);
            return Result.success(response);
        }
        catch (Exception e) {
            return Result.error("调用分析服务失败: " + e.getMessage());
        }

    }


    @GetMapping("/analysisList")
    public Result<PageBean<EegAnalysisResult>> list(
            @RequestParam Integer pageNum,
            @RequestParam Integer pageSize,
            @RequestParam(value = "searchQuery",required = false) String name
    ) {
        PageBean<EegAnalysisResult> pageData = eegService.list(pageNum, pageSize, name);
        return Result.success(pageData);
    }







}
