package com.medicine.medicinespringboot.service.Impl;

import com.medicine.medicinespringboot.pojo.Notification;

import java.util.List;

public interface NotificationService {
    void add(Notification notification);

    List<Notification> list();
}
