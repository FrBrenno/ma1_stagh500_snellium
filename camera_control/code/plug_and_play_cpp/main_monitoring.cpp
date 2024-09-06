#include <iostream>
#include <string>
#include <systemd/sd-device.h>

int enumerating_all_serial_ports()
{
    int ret = 0;
    // Enumerate all serial port devices
    sd_device_enumerator *enumerator = nullptr;
    ret = sd_device_enumerator_new(&enumerator);
    if (ret < 0)
    {
        std::cerr << "Failed to create device enumerator: " << strerror(-ret) << std::endl;
        return ret;
    }

    // Add filter for serial port devices
    ret = sd_device_enumerator_add_match_subsystem(enumerator, "tty", true);
    if (ret < 0)
    {
        std::cerr << "Failed to add match subsystem: " << strerror(-ret) << std::endl;
        return ret;
    }
    ret = sd_device_enumerator_add_match_subsystem(enumerator, "usb", true);
    if (ret < 0)
    {
        std::cerr << "Failed to add match subsystem: " << strerror(-ret) << std::endl;
        return ret;
    }

    // Enumerate devices
    sd_device *device = nullptr;
    int counter = 0;
    while (true)
    {
        if (counter == 0)
            device = sd_device_enumerator_get_device_first(enumerator);
        else
            device = sd_device_enumerator_get_device_next(enumerator);

        if (device == nullptr)
            break;

        // getting device name
        const char *device_name = nullptr;
        ret = sd_device_get_sysname(device, &device_name);
        if (ret < 0)
        {
            std::cerr << "Failed to get device name: " << strerror(-ret) << std::endl;
            return ret;
        }
        std::cout << "Device name: " << device_name << std::endl;
        counter++;
    }

    // Free resources
    sd_device_unref(device);
    sd_device_enumerator_unref(enumerator);

    std::cout << "Found " << counter << " serial port devices." << std::endl;
    return 0;
}

int i = 0;

int device_event_callback(sd_device_monitor *monitor, sd_device *device, void *userdata)
{
    int ret;

    std::cout << i << " == Device event callback" << std::endl;
    i++;
    // getting device name
    const char *device_name = nullptr;
    ret = sd_device_get_sysname(device, &device_name);
    if (ret < 0)
    {
        std::cerr << "Failed to get device name: " << strerror(-ret) << std::endl;
        return ret;
    }
    std::cout << "Device name: " << device_name << std::endl;

    // getting device action
    sd_device_action_t device_action;
    ret = sd_device_get_action(device, &device_action);
    if (ret < 0)
    {
        std::cerr << "Failed to get device action: " << strerror(-ret) << std::endl;
        return ret;
    }
    std::cout << "Device action: ";
    switch (device_action)
    {
    case SD_DEVICE_ADD:
        std::cout << "added" << std::endl;
        break;
    case SD_DEVICE_REMOVE:
        std::cout << "removed" << std::endl;
        break;
    default:
        std::cout << "unknown" << std::endl;
        break;
    }

    return 0;
}

/**
 * @brief Asynchronously monitor serial ports list changes
 */
int monitoring_serial_ports()
{
    int ret = 0;

    sd_event *event = nullptr;
    sd_device_monitor *monitor = nullptr;

    ret = sd_event_new(&event);
    if (ret < 0)
    {
        std::cerr << "Failed to create event loop: " << strerror(-ret) << std::endl;
        return ret;
    }
    ret = sd_device_monitor_new(&monitor);
    if (ret < 0)
    {
        std::cerr << "Failed to create device monitor: " << strerror(-ret) << std::endl;
        return ret;
    }
    ret = sd_device_monitor_filter_add_match_subsystem_devtype(monitor, "tty", nullptr);
    if (ret < 0)
    {
        std::cerr << "Failed to add match subsystem: " << strerror(-ret) << std::endl;
        return ret;
    }
    ret = sd_device_monitor_attach_event(monitor, event);
    if (ret < 0)
    {
        std::cerr << "Failed to attach event loop: " << strerror(-ret) << std::endl;
        return ret;
    }
    ret = sd_device_monitor_start(monitor, device_event_callback, nullptr);
    if (ret < 0)
    {
        std::cerr << "Failed to start device monitor: " << strerror(-ret) << std::endl;
        return ret;
    }

    while (true)
    {
        ret = sd_event_loop(event);
        if (ret < 0)
        {
            std::cerr << "Failed to run event loop: " << strerror(-ret) << std::endl;
            return ret;
        }
    }

    return 0;
}

int main()
{
    int ret = 0;

    // ret = enumerating_all_serial_ports();

    ret = monitoring_serial_ports();

    return ret;
}