package com.medicine.medicinespringboot.utils;



import com.google.gson.Gson;
import com.qiniu.common.QiniuException;
import com.qiniu.http.Response;
import com.qiniu.storage.BucketManager;
import com.qiniu.storage.Configuration;
import com.qiniu.storage.Region;
import com.qiniu.storage.UploadManager;
import com.qiniu.storage.model.DefaultPutRet;
import com.qiniu.util.Auth;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;


@Slf4j
@Component
public class QiniuUtil {
    // 通过 @Value 注解从配置文件中读取值
    @Value("${qiniu.accessKey}")
    private String accessKey;

    @Value("${qiniu.secretKey}")
    private String secretKey;

    @Value("${qiniu.bucket}")
    private String bucket;

    @Value("${qiniu.hostName}")
    private String hostName;

    public String uploadByBytes(byte[] bytes,String fileName){

        //构造一个带指定 Region 对象的配置类
        Configuration cfg = new Configuration(Region.qvmHuabei());
        cfg.resumableUploadAPIVersion = Configuration.ResumableUploadAPIVersion.V2;// 指定分片上传版本
        UploadManager uploadManager = new UploadManager(cfg);

        //默认不指定key的情况下，以文件内容的hash值作为文件名
        String key = fileName;

        Auth auth = Auth.create(accessKey, secretKey);
        String upToken = auth.uploadToken(bucket);

        try {
            Response response = uploadManager.put(bytes, key, upToken);
            //解析上传成功的结果
            DefaultPutRet putRet = new Gson().fromJson(response.bodyString(), DefaultPutRet.class);
            System.out.println(putRet.key);
            System.out.println(putRet.hash);
            return hostName+putRet.key;
        } catch (QiniuException ex) {
            ex.printStackTrace();
            if (ex.response != null) {
                System.err.println(ex.response);
                try {
                    String body = ex.response.toString();
                    System.err.println(body);
                } catch (Exception ignored) {
                }
            }
        }
        return null;
    }

    /**
     * 直接删除方法（假设URL已校验）
     * @param fileUrl 保证有效的文件URL
     * @return 操作结果
     */
    public String deleteFileDirect(String fileUrl) {
        BucketManager bucketManager = new BucketManager(Auth.create(accessKey, secretKey), new Configuration(Region.qvmHuabei()));
        String key = extractKeyDirect(fileUrl);
        try {
            bucketManager.delete(bucket, key);
            log.info("文件删除成功 || Key: {}", key);
            return "success";
        } catch (QiniuException e) {
            log.error("删除操作失败 || Key: {} || 错误码: {}", key, e.code(), e);
            return "failed: " + e.code();
        }
    }

    /**
     * 直接提取Key（基于字符串处理）
     */
    private String extractKeyDirect(String fileUrl) {
        // 移除协议头和域名部分
        String cleanUrl = fileUrl
                .replaceFirst("https?://[^/]+", "")  // 移除协议和域名
                .split("[?#]")[0];                   // 移除查询参数和锚点

        // 解码URL特殊字符
        return URLDecoder.decode(cleanUrl, StandardCharsets.UTF_8)
                .replaceAll("^/+", "");              // 移除开头斜杠
    }



}