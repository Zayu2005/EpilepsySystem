package com.medicine.medicinespringboot;

import java.util.Scanner;

public class PopulationProjection {
    public static void main(String[] args) {
        int birthPerSeconds = 7;    //每7秒有一个人诞生
        int diePerSeconds = 13;    //每13秒一个人死亡
        int migrationSeconds = 13;    //每45秒一个人移民

        //当前人口
        int currentPopulation = 312032486;
        int secondsPerYear = 365 * 24 * 60 * 60;

        //计算每年的人口变化量
        int birthPerYear = secondsPerYear / birthPerSeconds;
        int diePerYear = secondsPerYear / diePerSeconds;
        int migrationPerYear = secondsPerYear / migrationSeconds;

        int times = 5;
        while(times > 0){
            currentPopulation = currentPopulation + birthPerYear - diePerYear + migrationPerYear;
            System.out.println("第"+times+"年的人口数量为:"+ currentPopulation);
            times--;
        }
    }
}