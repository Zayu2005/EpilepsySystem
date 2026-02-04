package com.medicine.medicinespringboot.mapper;


import com.medicine.medicinespringboot.pojo.EegFeaturesFile;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface FeatureMapper {



    @Insert("INSERT INTO eeg_features_files(url, user_id, patient_id, create_time) " +
            "VALUES(#{url},#{userId},#{patientId},now())")
    void add(Integer patientId, Integer userId, String url);


    @Select("SELECT * FROM eeg_features_files WHERE patient_id = #{patientId} AND user_id = #{userId}")
    EegFeaturesFile findByPatientIdAndUserId(Integer patientId, Integer userId);



    @Update("UPDATE eeg_features_files SET url = #{url} WHERE patient_id = #{patientId} AND user_id = #{userId}")
    void updateUrl(Integer patientId, Integer userId, String url);
}
