import os
import terrascript
import json

from utils import get_yaml_input, generate_terraform_backend_provider_and_label
from setup_input_kwargs import setup_input_kwargs
from tfprompts import user_confirmation

def tf_generate_and_run(build_data):
    """
    Using python-terraform package we can invoke terraform statements
    such as terraform init, plan, apply etc. in python code
    :param build_data:
    :return:
    """
    build_modules = build_data["modules"]

    # loop through each selected module(s) e.g. "./components/management/secrets/kms.yaml" process to ---> kms
    mods = []
    for m in build_modules:
        print("\n\n****************************************************************************")
        print("Permforming action \"{0}\" for module {1}".format(build_data["tfaction"], m))
        print("****************************************************************************\n\n")
        mod1 = (m.split('/')[-1])
        module_name = mod1.split('.')[0]
        mods.append(module_name)

    for m in mods:
        generate_module(m, build_data)
        run_module(m, build_data)


def generate_module(module_name, build_data):

    ts = terrascript.Terrascript()
    workspace = build_data["workspace"]

    global_data, src_data, labels_data, mod_data = get_yaml_input(module_name, build_data)

    if module_name == "s3_tfstate_backend":
        ts, label, label_kwargs = generate_terraform_backend_provider_and_label(module_name, build_data, ts, add_backend=False)
    else:
        ts, label, label_kwargs = generate_terraform_backend_provider_and_label(module_name, build_data, ts)

    # setup key words arguments input parameters...
    input_kwargs = setup_input_kwargs(module_name, build_data, src_data, mod_data, ts)

    # generate terraform codes to invoke opensource/in-house terraform modules
    ts += terrascript.Module(_name=module_name, **input_kwargs)

    if "destroy" not in build_data['tfaction']:
        # generate module outputs
        for field in mod_data[workspace]['module']['outputs']:
            ts += terrascript.Output(field, value="{0}module.{1}.{2}{3}".format("${", module_name, field, "}"))

    # generate main.tf.json file in the generated directory
    generate_main_tf_file(module_name, ts, build_data)


def generate_main_tf_file(module_name, terrascript, build_data):

    gen_path = build_data["gen_path"]
    workspace = build_data["workspace"]
    gen_module_path = f"{gen_path}/{module_name}/{workspace}"
    main_json_file = f"{gen_module_path}/main.tf.json"

    os.system(f"mkdir -p {gen_module_path}")
    os.system(f"rm -rf {gen_module_path}/.terraform")

    file = open(main_json_file, "w")
    file.write(json.dumps(terrascript, indent=2, sort_keys=False))
    file.close()


def run_module(module_name, build_data):
    """
    Loop through list of selected module(s) and build based on the selected account
    :return:
    """
    gen_path = build_data["gen_path"]
    workspace = build_data["workspace"]
    gen_module_path = f"{gen_path}/{module_name}/{workspace}"
    plan_output_file = "plan.out"

    remove_prev_run = f"cd {gen_module_path} && rm -f {plan_output_file} && rm -rf .terraform"
    os.system(remove_prev_run)

    tf_plan_cmd = f"cd {gen_module_path} && terraform workspace new {workspace} || terraform workspace select {workspace} && terraform plan -out {plan_output_file}"
    tf_plan_destroy_cmd = f"cd {gen_module_path} && terraform workspace new {workspace} || terraform workspace select {workspace} && terraform plan -destroy -out {plan_output_file}"
    tf_apply_cmd = f"cd {gen_module_path} && terraform workspace new {workspace} || terraform workspace select {workspace} && terraform apply {plan_output_file}"
    tf_init_cmd = f"cd {gen_module_path} && terraform init && terraform workspace new {workspace} || terraform workspace select {workspace}"
    print(tf_init_cmd)

    os.system(tf_init_cmd)

    if build_data["tfaction"] == 'plan':
        # always auto approve 'plan' action
        os.system(tf_plan_cmd)
    elif build_data["tfaction"] == 'plan-destroy':
        # always auto approve 'plan' action
        os.system(tf_plan_destroy_cmd)
    elif build_data["tfaction"] == 'apply':
        if build_data["auto_approve"]:
            # auto-approve flag enabled so skip user confirmation
            os.system(tf_plan_cmd)
            os.system(tf_apply_cmd)
        else:
            os.system(tf_plan_cmd)
            # confirm with user first
            if user_confirmation("Sure you want to APPLY {0}".format(module_name)):
                os.system(tf_apply_cmd)
            else:
                print("User aborting...")
    elif build_data["tfaction"] == 'apply-destroy':
        if build_data["auto_approve"]:
            os.system(tf_plan_cmd)
            os.system(tf_apply_cmd)
        else:
            # confirm with user first
            os.system(tf_plan_destroy_cmd)
            if user_confirmation("Sure you want to APPLY DESTROY {0}".format(module_name)):
                os.system(tf_apply_cmd)
            else:
                print("User aborting...")

