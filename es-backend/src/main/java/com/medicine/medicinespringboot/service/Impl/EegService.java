package com.medicine.medicinespringboot.service.Impl;

import com.medicine.medicinespringboot.pojo.EegAnalysis;
import com.medicine.medicinespringboot.pojo.EegAnalysisResult;
import com.medicine.medicinespringboot.pojo.PageBean;

import java.util.Map;

public interface EegService {
    void add(Integer patientId, Integer userId, String url);

    EegAnalysis findAnalysisByPatientId(Integer patientId);

    void saveAnalysisResult(Map<String, Object> response,Integer patientId, Integer userId);

    PageBean<EegAnalysisResult> list(Integer pageNum, Integer pageSize, String name);

    EegAnalysis findEegByPatientIdAndUserId(Integer patientId, Integer userId);

    void update(Integer patientId, Integer userId, String url);
}
