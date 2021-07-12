from flask import Blueprint, flash
from flask import render_template, redirect, url_for, request
from app import app
from app.forms import CreateApplication, SearchOneItem, EditApplication, RegistrationDeviceForm, ActivationDeviceForm
from flask_login import current_user, login_required
from app.models import *
from config import Configuration
from sqlalchemy.exc import IntegrityError

import json
import requests

app.config.from_object(Configuration)
service = Blueprint('service', __name__, template_folder='templates')


api_url_base = app.config['API_URL_BASE']


##########################################################################################################
#                                            UNI FUNCTION                                                #
##########################################################################################################


# GET only one item with unique ID
def get_one_item(url, headers):
    api_url = f"{api_url_base}{url}"
    response = requests.get(api_url, headers=headers)
    if response.status_code >= 500:
        flash(f'[!] [{response.status_code}] Server Error')
        return None
    elif response.status_code == 404:
        flash(f'[!] [{response.status_code}] URL not found: [{api_url}]')
        return None
    elif response.status_code == 401:
        flash(f'[!] [{response.status_code}] Authentication Failed')
        return None
    elif response.status_code == 400:
        flash(f'[!] [{response.status_code}] Bad Request or invalid character "s" looking for beginning of value')
        return None
    elif response.status_code >= 300:
        flash(f'[!] [{response.status_code}] Unexpected Redirect')
        return None
    elif response.status_code == 200:
        one_item = json.loads(response.content.decode('utf-8'))
        return one_item
    else:
        flash(f'[?] Unexpected Error: [HTTP {response.status_code}]: Content: {response.content}')
    return None


# DELETE one item with unique ID
def delete_item(url, headers):
    api_url = f"{api_url_base}{url}"
    response = requests.delete(api_url, headers=headers)

    if response.status_code >= 500:
        flash(f'[!] [{response.status_code}] Server Error')
        return None
    elif response.status_code == 404:
        flash(f'[!] [{response.status_code}] URL not found: [{api_url}]')
        return None
    elif response.status_code == 401:
        flash(f'[!] [{response.status_code}] Authentication Failed')
        return None
    elif response.status_code == 400:
        flash(f'[!] [{response.status_code}] Bad Request or invalid character "s" looking for beginning of value')
        return None
    elif response.status_code >= 300:
        flash(f'[!] [{response.status_code}] Unexpected Redirect')
        return None
    elif response.status_code == 200:
        delete_one_item = json.loads(response.content)
        return response.status_code
    else:
        flash(f'[?] Unexpected Error: [HTTP {response.status_code}]: Content: {response.content}')
    return None


# Universal function for GET
def get_uni(url, headers):
    api_url = f"{api_url_base}{url}"
    response = requests.get(api_url, headers=headers)

    if response.status_code >= 500:
        flash(f'[!] [{response.status_code}] Server Error')
        return None
    elif response.status_code == 404:
        flash(f'[!] [{response.status_code}] URL not found: [{api_url}]')
        return None
    elif response.status_code == 401:
        flash(f'[!] [{response.status_code}] Authentication Failed')
        return None
    elif response.status_code == 400:
        flash(f'[!] [{response.status_code}] Bad Request or invalid character "s" looking for beginning of value')
        return None
    elif response.status_code >= 300:
        flash(f'[!] [{response.status_code}] Unexpected Redirect')
        return None
    elif response.status_code == 200:
        list_of_items = json.loads(response.content.decode('utf-8'))
        return list_of_items
    else:
        flash(f'[?] Unexpected Error: [HTTP {response.status_code}]: Content: {response.content}')
    return None


# Universal function for POST
def post_uni(url, headers, dict_items):
    api_url = f"{api_url_base}{url}"
    response = requests.post(api_url, headers=headers, json=dict_items)

    if response.status_code >= 500:
        flash(f'[!] [{response.status_code}] Server Error')
        return None
    elif response.status_code >= 409:
        flash(f'[!] [{response.status_code}] Object already exists')
        return None
    elif response.status_code == 404:
        flash(f'[!] [{response.status_code}] URL not found: [{api_url}]')
        return None
    elif response.status_code == 401:
        flash(f'[!] [{response.status_code}] Authentication Failed')
        return None
    elif response.status_code >= 400:
        flash(f'[!] [{response.status_code}] Bad Request or invalid character "s" looking for beginning of value.')
        return None
    elif response.status_code >= 300:
        flash(f'[!] [{response.status_code}] Unexpected redirect.')
        return None
    elif response.status_code == 200:
        update_item = json.loads(response.content)
        return response.status_code
    else:
        flash(f'[?] Unexpected Error: [HTTP {response.status_code}]: Content: {response.content}')
        return None


# Universal function for edit any item
def put_uni(url, headers, dict_items):
    api_url = f"{api_url_base}{url}"
    response = requests.put(api_url, headers=headers, json=dict_items)

    if response.status_code >= 500:
        flash(f'[!] [{response.status_code}] Server Error')
        return None
    elif response.status_code >= 409:
        flash(f'[!] [{response.status_code}] Object already exists')
        return None
    elif response.status_code == 404:
        flash(f'[!] [{response.status_code}] URL not found: [{api_url}]')
        return None
    elif response.status_code == 401:
        flash(f'[!] [{response.status_code}] Authentication Failed')
        return None
    elif response.status_code >= 400:
        flash(f'[!] [{response.status_code}] Bad Request or invalid character "s" looking for beginning of value')
        return None
    elif response.status_code >= 300:
        flash(f'[!] [{response.status_code}] Unexpected redirect.')
        return None
    elif response.status_code == 200:
        added_item = json.loads(response.content)
        return response.status_code
    else:
        flash(f'[?] Unexpected Error: [HTTP {response.status_code}]: Content: {response.content}')
        return None


##########################################################################################################
#                                            APPLICATION SERVICE                                         #
##########################################################################################################


# Main page
@service.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        get_api_token = request.form.get('api_token')
        current_user.api_token = get_api_token
        db.session.commit()
        flash("The api token is changed!")
        return redirect(url_for('service.index'))

    return render_template('service/index.html')


# Get information about applications
@service.route('/get_applications', methods=['POST', 'GET'])
@login_required
def get_applications():
    api_token = current_user.api_token
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_token}'}

    url = "api/applications?limit=10"
    list_applications = get_uni(url=url, headers=headers)

    form = SearchOneItem(request.form)

    if request.method == 'POST':
        id_item = request.form.get('id_item')

        return redirect(url_for('service.edit_application', application_id=id_item))

    return render_template('service/get_applications.html', form=form, list_applications=list_applications)


# Create new application
@service.route('/create_application', methods=["POST", "GET"])
@login_required
def create_application():
    api_token = current_user.api_token
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_token}'}

    url = "api/applications"
    app_item = {'application': {}}
    form = CreateApplication()

    if form.validate_on_submit():
        app_item['application']['description'] = form.description.data
        app_item['application']['id'] = form.id.data
        app_item['application']['name'] = form.name.data
        app_item['application']['organizationID'] = form.organizationID.data
        app_item['application']['serviceProfileID'] = form.serviceProfileID.data

        new_app = post_uni(url=url, headers=headers, dict_items=app_item)

        if new_app == 200:
            flash(f"Application: {app_item['application']['name']} was successfully created.")
            return redirect(url_for('service.index'))

    return render_template('service/create_application.html', title='Create Application', form=form)


# Edit an application, required an applicationID
@service.route('/edit_application/<application_id>', methods=['POST', 'GET'])
@login_required
def edit_application(application_id):
    api_token = current_user.api_token
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_token}'}

    url = f"api/applications/{application_id}"
    app_instance = {'application': {}}

    form = EditApplication(request.form)

    if form.validate_on_submit():
        app_instance['application']['description'] = form.description.data
        app_instance['application']['id'] = form.id.data
        app_instance['application']['name'] = form.name.data
        app_instance['application']['organizationID'] = form.organizationID.data
        app_instance['application']['serviceProfileID'] = form.serviceProfileID.data

        edit_app = put_uni(url=url, headers=headers, dict_items=app_instance)
        if edit_app == 200:
            flash(f"Application {request.form.get('name')} was changed.")
            return redirect(url_for('service.get_applications'))
    else:
        app_item = get_one_item(url=url, headers=headers)
        return render_template('service/edit_application.html', app_item=app_item, application_id=application_id)


# DELETE an application
@service.route('/delete_application/<application_id>')
@login_required
def delete_application(application_id):
    api_token = current_user.api_token
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_token}'}

    url = f"api/applications/{application_id}"

    del_app = delete_item(url, headers)
    if del_app == 200:
        flash(f"Application #{application_id} was deleted.")
    return redirect(url_for('service.get_applications'))

##########################################################################################################
#                                            DEVICE SERVICE                                              #
##########################################################################################################


# Registering a new device
@service.route('/register_device', methods=['GET', 'POST'])
@login_required
def register_device():
    api_token = current_user.api_token
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_token}'}

    new_device = {'device': {}}
    form = RegistrationDeviceForm()

    if form.validate_on_submit():
        # save all data from the form to the variable 'device'
        device = Device(device_EUI=form.device_EUI.data,
                        device_name=form.device_name.data,
                        description=form.description.data,
                        device_profile_id=form.device_profile_id.data,
                        application_id=form.application_id.data,
                        application_name=form.application_name.data,
                        user=current_user)
        # save all date from the form to the dictionary 'new_device' for registration on the server
        new_device['device']['applicationID'] = form.application_id.data
        new_device['device']['description'] = form.description.data
        new_device['device']['devEUI'] = form.device_EUI.data
        new_device['device']['deviceProfileID'] = form.device_profile_id.data
        new_device['device']['isDisabled'] = False
        new_device['device']['name'] = form.device_name.data
        new_device['device']['referenceAltitude'] = 0
        new_device['device']['skipFCntCheck'] = False
        new_device['device']['tags'] = {}
        new_device['device']['variables'] = {}

        # registration on the server
        url = "api/devices"
        result_registration = post_uni(url=url, headers=headers, dict_items=new_device)

        if result_registration == 200:
            # if registration was successful, save it to the database
            try:
                db.session.add(device)
                db.session.commit()
            except:
                print("Error occurred")

            flash('Congratulations, you have a new device registered now!')
            return redirect(url_for('service.get_devices'))
        else:
            flash("Try it again.")
            return redirect(url_for('service.register_device'))

    return render_template('service/register_device.html', form=form)


# After registration on the server, the device must be activated
@service.route('/device_activation', methods=['POST', 'GET'])
@login_required
def device_activation():
    api_token = current_user.api_token
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_token}'}

    dev_active = {"deviceActivation": {}}
    form = ActivationDeviceForm(request.form)

    # save all date from the form to the dictionary 'new_device' for activation on the server
    if form.validate_on_submit():
        dev_active['deviceActivation']['aFCntDown'] = 0
        dev_active['deviceActivation']['appSKey'] = request.form.get('appsskey')
        dev_active['deviceActivation']['devAddr'] = request.form.get('devaddrs')
        dev_active['deviceActivation']['devEUI'] = request.form.get('deveui')
        dev_active['deviceActivation']['fCntUp'] = 0
        dev_active['deviceActivation']['fNwkSIntKey'] = request.form.get('networksskey')
        dev_active['deviceActivation']['nFCntDown'] = 0
        dev_active['deviceActivation']['nwkSEncKey'] = request.form.get('networksskey')
        dev_active['deviceActivation']['sNwkSIntKey'] = request.form.get('networksskey')

        # the process of activation a device
        url = f"api/devices/{dev_active['deviceActivation'].get('devEUI')}/activate"
        result_activation = post_uni(url=url, headers=headers, dict_items=dev_active)

        if result_activation == 200:
            flash(f"Device with EUI '{dev_active['deviceActivation'].get('devEUI')}' is activated.")
            return redirect(url_for('service.index'))
        else:
            flash(f"{result_activation}")
            flash(f"Device with EUI '{dev_active['deviceActivation'].get('devEUI')}' was not activated.")
            return redirect(url_for('service.device_activation'))

    return render_template('service/device_activation.html', form=form)


# Get a list of devices from the server
@service.route('/get_devices', methods=['POST', 'GET'])
@login_required
def get_devices():
    api_token = current_user.api_token
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_token}'}
    url = "api/applications?limit=10"

    list_applications = get_uni(url=url, headers=headers)
    devices_dict = {'devices': []}

    for item in list_applications['result']:
        url = f"api/devices?limit=10&applicationID={item['id']}"
        list_devices = get_uni(url=url, headers=headers)

        # Update devices database from LoRaWAN Server
        if list_devices:
            for device in list_devices['result']:
                mot = Device.query.filter_by(device_EUI=device.get('devEUI')).first()
                if mot:
                    mot.device_battery = device.get('deviceStatusBatteryLevel')

                try:
                    db.session.commit()
                except:
                    flash(f"Can not update device {device.get('devEUI')}")
                else:
                    mot = Device(device_EUI=device.get('devEUI'),
                                 device_name=device.get('name'),
                                 description=device.get('description'),
                                 device_profile_id=device.get('deviceProfileID'),
                                 device_profile_name=device.get('deviceProfileName'),
                                 device_battery=device.get('deviceStatusBatteryLevel'),
                                 application_id=device.get('applicationID'),
                                 application_name=item.get('name'),
                                 user=current_user)
                    try:
                        db.session.add(mot)
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()

        else:
            flash("Maybe you have a wrong api token.")

    for mot in Device.query.all():
        item_of_device = {'devEUI': mot.device_EUI,
                          'name': mot.device_name,
                          'applicationID': mot.application_id,
                          'description': mot.description,
                          'deviceProfileID': mot.device_profile_id,
                          'deviceProfileName': mot.device_profile_name,
                          'deviceStatusBattery': mot.device_battery,
                          'lastSeenAt': mot.timestamp}
        devices_dict['devices'].append(item_of_device)

    total_count = len(devices_dict['devices'])

    form = SearchOneItem()

    if request.method == 'POST':
        dev_eui = request.form.get('del_id_item')
        return redirect(url_for('service.delete_device', device_eui=dev_eui))

    return render_template('service/get_devices.html',
                           device_dict=devices_dict,
                           total_count=total_count,
                           form=form)


@service.route('/delete_device/<device_eui>')
@login_required
def delete_device(device_eui):
    api_token = current_user.api_token
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_token}'}

    device = Device.query.filter_by(device_EUI=device_eui).first()

    # Delete device from database
    try:
        db.session.delete(device)
        db.session.commit()
        flash("The device was deleted from local database.")

        # Delete device from Lora server
        url = f"api/devices/{device_eui}"
        del_device = delete_item(url=url, headers=headers)
        if del_device == 200:
            flash("The device was deleted from Lora server.")
    except:
        print(f"An error occurred when try delete device #{device.device_EUI}")

    return redirect(url_for('service.get_devices'))


@service.route('/device_date/<device_eui>')
def device_data(device_eui):
    # Set the pagination configuration
    device = Device.query.filter_by(device_EUI=device_eui).first_or_404()
    page = request.args.get('page', 1, type=int)
    dates = device.device_data.order_by(DeviceData.timestamp.desc()).paginate(
            page, app.config['ROWS_PER_PAGE'], False)

    return render_template('service/device_data.html', device=device, device_eui=device_eui, dates=dates)



