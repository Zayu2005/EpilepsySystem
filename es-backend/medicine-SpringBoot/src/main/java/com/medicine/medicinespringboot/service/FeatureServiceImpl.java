package com.medicine.medicinespringboot.service;

import com.medicine.medicinespringboot.mapper.FeatureMapper;
import com.medicine.medicinespringboot.pojo.EegFeaturesFile;
import com.medicine.medicinespringboot.service.Impl.FeatureService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


@Service
public class FeatureServiceImpl implements FeatureService {

    @Autowired
    private FeatureMapper featureMapper;
    @Override
    public void add(Integer patientId, Integer userId, String url) {
        featureMapper.add(patientId, userId, url);
    }

    @Override
    public EegFeaturesFile findByPatientIdAndUserId(Integer patientId, Integer userId) {
        return featureMapper.findByPatientIdAndUserId(patientId, userId);
    }

    @Override
    public void updateUrl(Integer patientId, Integer userId, String url) {
        featureMapper.updateUrl(patientId, userId, url);
    }
}
