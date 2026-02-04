package com.medicine.medicinespringboot.service;


import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.medicine.medicinespringboot.mapper.EegMapper;
import com.medicine.medicinespringboot.pojo.Anomaly;
import com.medicine.medicinespringboot.pojo.EegAnalysis;
import com.medicine.medicinespringboot.pojo.EegAnalysisResult;
import com.medicine.medicinespringboot.pojo.PageBean;
import com.medicine.medicinespringboot.service.Impl.EegService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

@Service
public class EegServiceImpl implements EegService {

    @Autowired
    private EegMapper eegMapper;

    @Override
    public void add(Integer patientId, Integer userId, String url) {
        eegMapper.add(patientId, userId, url);
    }

    @Override
    public EegAnalysis findAnalysisByPatientId(Integer patientId) {
        return eegMapper.findAnalysisByPatientId(patientId);
    }

    @Override
    public void saveAnalysisResult(Map<String, Object> response,Integer patientId, Integer userId) {
//        //将结果保存到数据库中
//        Map<String, Object> data = (Map<String, Object>) response.get("data");
//        EegAnalysisResult eegAnalysisResult = new EegAnalysisResult();
//        //提取数据到eegAnalysisResult中
//        eegAnalysisResult.setFileName((String) data.get("file_name"));
//        eegAnalysisResult.setFileSize(((Integer) data.get("file_size")).longValue()); // Integer → Long
//        eegAnalysisResult.setStartTime(((Number) data.get("start_time")).doubleValue()); // 兼容 Integer/Double
//        eegAnalysisResult.setEndTime(((Number) data.get("end_time")).doubleValue());
//        eegAnalysisResult.setDischargeCount((Integer) data.get("dischargeCount"));
//        eegAnalysisResult.setRhythm((String) data.get("rhythm"));
//        eegAnalysisResult.setFrequency((String) data.get("frequency"));
//        eegAnalysisResult.setRiskLevel((Integer) data.get("riskLevel"));
//        //处理anomalies列表
//        List<Map<String, Object>> anomaliesData = (List<Map<String, Object>>) data.get("anomalies");
//        List<Anomaly> anomalies = new ArrayList<>();
//        System.out.println(Arrays.toString(anomaliesData.toArray()));
//        for (Map<String, Object> anomalyData : anomaliesData) {
//            Anomaly anomaly = new Anomaly();
//            anomaly.setType((String) anomalyData.get("type"));
//            anomaly.setSeverity((String) anomalyData.get("severity"));
//            anomalies.add(anomaly);
//        }
//
//        //最终数据
//        eegAnalysisResult.setAnomalies(anomalies);
//        eegMapper.saveAnalysisResult(eegAnalysisResult);
        // 提取 data 字段
        Map<String, Object> data = (Map<String, Object>) response.get("data");

        // 构建主表对象
        EegAnalysisResult result = new EegAnalysisResult();
        result.setPatientId(patientId);
        result.setUserId(userId);
        result.setFileName((String) data.get("file_name"));
        result.setFileSize(((Integer) data.get("file_size")).longValue());
        result.setStartTime(((Number) data.get("start_time")).doubleValue());
        result.setEndTime(((Number) data.get("end_time")).doubleValue());
        result.setDischargeCount((Integer) data.get("dischargeCount"));
        result.setRhythm((String) data.get("rhythm"));
        result.setFrequency((String) data.get("frequency"));
        result.setRiskLevel((Integer) data.get("riskLevel"));

        // 插入主表并获取自增 ID
        eegMapper.insertAnalysisResult(result);

        // 处理子表（anomalies）
        List<Map<String, Object>> anomaliesData = (List<Map<String, Object>>) data.get("anomalies");
        if (anomaliesData != null && !anomaliesData.isEmpty()) {
            List<Anomaly> anomalies = new ArrayList<>();
            for (Map<String, Object> anomalyData : anomaliesData) {
                Anomaly anomaly = new Anomaly();
                anomaly.setAnalysisId(result.getId()); // 设置外键
                anomaly.setType((String) anomalyData.get("type"));
                anomaly.setSeverity((String) anomalyData.get("severity"));
                anomalies.add(anomaly);
            }
            eegMapper.batchInsertAnomalies(anomalies);
        }
    }

    @Override
    public PageBean<EegAnalysisResult> list(Integer pageNum, Integer pageSize, String name) {
            // 启动分页
            PageHelper.startPage(pageNum, pageSize);

            // 执行查询
            List<EegAnalysisResult> analysisResults = eegMapper.selectAnalysisResultPage(name);

            // 获取分页信息
            Page<EegAnalysisResult> page = (Page<EegAnalysisResult>) analysisResults;

            //为每个结果加载关联的异常数据
            analysisResults.forEach(result -> {
                List<Anomaly> anomalies = eegMapper.selectAnomaliesByAnalysisId(result.getId());
                result.setAnomalies(anomalies);
            });

            //封装到自定义 PageBean
            return new PageBean<>(page.getTotal(), page.getResult());
    }

    @Override
    public EegAnalysis findEegByPatientIdAndUserId(Integer patientId, Integer userId) {

        return eegMapper.findEegByPatientIdAndUserId(patientId, userId);
    }

    @Override
    public void update(Integer patientId, Integer userId, String url) {
        eegMapper.update(patientId, userId, url);
    }
}
