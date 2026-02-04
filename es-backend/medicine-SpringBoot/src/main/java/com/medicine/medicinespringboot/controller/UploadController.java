package com.medicine.medicinespringboot.controller;


import com.medicine.medicinespringboot.pojo.Result;
import com.medicine.medicinespringboot.utils.QiniuUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.util.UUID;


@Controller
public class UploadController {

    @Autowired
    private QiniuUtil qiniuUtil;


    @ResponseBody
    @PostMapping("upload")
    public Result upload(MultipartFile multipartFile) throws IOException {
        //获取文件名称
        String originalFilename = multipartFile.getOriginalFilename();
        //获取后缀名
        String suffix = originalFilename.substring(originalFilename.lastIndexOf("."));
        //为了避免同名覆盖问题,构建新的文件名
        String fileName = UUID.randomUUID().toString() + suffix;

        //调用七牛云OSS工具类
        String url = qiniuUtil.uploadByBytes(multipartFile.getBytes(),fileName);
        //将图片上传完成后的url返回，用于浏览器回显展示
        return Result.success(url);
    }
}