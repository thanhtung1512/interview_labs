import boto3
import logging
import traceback
import settings

logging.basicConfig(level=settings.LOGGING_LEVEL)

def sg_check_port(sg, port_number):
    """ Check security group has allowed specific port and CIDR """
    try:
        sg_desc = sg.ip_permissions[0]
        if 'FromPort' in sg_desc and 'IpRanges' in sg_desc:
            if sg_desc['FromPort'] == port_number and sg_desc['IpRanges'] == settings.CIDR_IP:
                return sg  
    except Exception as e:
        logging.error(traceback.format_exc()) 

def sg_check_tag(sg, tag_name, tag_value):
    """ Check security group has special tag name """
    try:
        sg_tag = sg.tags
        if sg.tags and sg_tag[0]['Key'] == tag_name and sg_tag[0]['Value'] == tag_value:
            return sg
    except Exception as e:
        logging.error(traceback.format_exc())
        
def sg_remove(sg, region):
    """ Remove security group """
    try:
        client = boto3.client('ec2', region_name=region)
        client.delete_security_group(GroupId=sg.id, DryRun=False)
    except Exception as e:
        logging.error(traceback.format_exc()) 


if __name__ == "__main__":
    """ Main function """
    sg_list = []
    regions = settings.REGIONS
    count_delete_sg = 0
    try:
        for region in regions:
            ec2 = boto3.resource('ec2', region_name=region)
            sgs = list(ec2.security_groups.all())
            for sg in sgs:
                if sg_check_port(sg, settings.SSH_PORT_NUMBER) and sg_check_tag(sg, settings.TAG_NAME, settings.TAG_VALUE):
                    sg_remove(sg, region) # Remove violated sg
                    print(f'Security Group: {sg.id} was deleted')
                    logging.info(f'count_delete_sg: ${count_delete_sg}')
                    count_delete_sg +=1
        
    except Exception as e:
        logging.error(traceback.format_exc())
                    
    if count_delete_sg < 1:
        logging.info("Not found any security group violated policy")
