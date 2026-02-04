package com.medicine.medicinespringboot.service.Impl;

import com.medicine.medicinespringboot.pojo.EegFeaturesFile;

public interface FeatureService {
    void add(Integer patientId, Integer userId, String url);

    EegFeaturesFile findByPatientIdAndUserId(Integer patientId, Integer userId);

    void updateUrl(Integer patientId, Integer userId, String url);
}
