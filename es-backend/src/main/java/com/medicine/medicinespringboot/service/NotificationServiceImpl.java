package com.medicine.medicinespringboot.service;

import com.medicine.medicinespringboot.mapper.NotificationMapper;
import com.medicine.medicinespringboot.pojo.Notification;
import com.medicine.medicinespringboot.service.Impl.NotificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class NotificationServiceImpl implements NotificationService {
    @Autowired
    private NotificationMapper notificationMapper;
    @Override
    public void add(Notification notification) {
        notificationMapper.add(notification);
    }

    @Override
    public List<Notification> list() {
        return notificationMapper.list();
    }
}
