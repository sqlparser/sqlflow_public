package com.gudusoft.grabit.util;

import java.text.SimpleDateFormat;
import java.util.Date;

public class DateUtil {
    public DateUtil() {
    }

    public static String format(Date date) {
        return format(date, "yyyyMMdd");
    }

    public static String format(Date date, String pattern) {
        if (date != null) {
            SimpleDateFormat df = new SimpleDateFormat(pattern);
            return df.format(date);
        } else {
            return null;
        }
    }

    public static String timeStamp2Date(Long seconds) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd");
        return sdf.format(new Date(seconds));
    }

}
