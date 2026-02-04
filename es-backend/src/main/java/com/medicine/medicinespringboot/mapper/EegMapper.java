package com.medicine.medicinespringboot.mapper;





import com.medicine.medicinespringboot.pojo.Anomaly;
import com.medicine.medicinespringboot.pojo.EegAnalysis;
import com.medicine.medicinespringboot.pojo.EegAnalysisResult;
import org.apache.ibatis.annotations.*;

import java.util.List;


@Mapper
public interface EegMapper {

    @Insert("insert into eeg_analysis(patient_id,user_id,url,create_time) values(#{patientId},#{userId},#{url}, NOW())")
    void add(Integer patientId, Integer userId, String url);


    @Select("select * from eeg_analysis where patient_id=#{patientId} ORDER BY create_time DESC LIMIT 1")
    EegAnalysis findAnalysisByPatientId(Integer patientId);

    void saveAnalysisResult(EegAnalysisResult eegAnalysisResult);

    // 批量插入异常数据（eeg_anomaly）
    void batchInsertAnomalies(@Param("anomalies") List<Anomaly> anomalies);

    void insertAnalysisResult(EegAnalysisResult result);


    // 分页查询
    List<EegAnalysisResult> selectAnalysisResultPage(@Param("name") String name);

    // 查询异常列表
    List<Anomaly> selectAnomaliesByAnalysisId(Integer analysisId);

    @Select("SELECT * FROM eeg_analysis WHERE patient_id = #{patientId} AND user_id = #{userId} ORDER BY create_time DESC LIMIT 1")
    EegAnalysis findEegByPatientIdAndUserId(Integer patientId, Integer userId);

    @Update("UPDATE eeg_analysis SET url = #{url} WHERE patient_id = #{patientId} AND user_id = #{userId} ORDER BY create_time DESC LIMIT 1")
    void update(Integer patientId, Integer userId, String url);
}
