from retinaface import RetinaFace
import cv2 
import numpy as np
import os
import time


# https://sefiks.com/2021/04/27/deep-face-detection-with-retinaface-in-python/


COMPRESSION_LEVEL=99
QUALITY=99


def blureFace_dir(car_diretory,fd_threshold,LOGGER):

    faces=[]
    flvl=os.listdir(f'{car_diretory}')
    for dir in flvl:
        
        dir_path = os.path.join(car_diretory, f'{dir}/1')
        images=os.listdir(dir_path)
        i=1
        for img in images:
            blurred_images=[]
            img_path=os.path.join(dir_path,img)
            
            if os.path.isfile(f'{img_path}'):

                    image=cv2.imread(img_path)
                    LOGGER.info('face detection started')
                    resp = RetinaFace.detect_faces(image,threshold=fd_threshold)
                    LOGGER.info('face detection ended')
                    i+=1
                    for identity in resp:
                        LOGGER.info('image blurring started')
                        try:
                            facial_area = resp[identity]['facial_area']   
                            blurred=cv2.GaussianBlur(image,(71,71),500)
                            faces.append(facial_area)

                        except KeyError:
                            LOGGER.info(f"KeyError: The key '{identity}' or 'facial_area' is missing in the response.")
                           

                        except cv2.error as e:
                            LOGGER.info(f"OpenCV error occurred: {e}")
                            
                        except FileNotFoundError as e:
                            LOGGER.info(f"File not found error: {e}")
                            
                        except Exception as e:
                            LOGGER.info(f"An unexpected error occurred: {e}")
                            
                              
                        try:
                            # Get detected face area from retinaFace response and assign face region to face veriable
                            x1, y1, x2, y2 = facial_area
                        
                            face = image[y1:y2, x1:x2]

                            #blur the face region
                            
                            # Create circular mask of the same size as the blurred image
                            mask = np.zeros_like(blurred)
                            h, w = face.shape[:2]
                            center = ((x1+w//2), (y1+h//2))
                            
                            cv2.ellipse(mask,center,(w//2,h//2),0,0,360, (255, 255, 255), -1)
                            
                            #create a circular blurred section
                            blurred_circular = cv2.bitwise_and(blurred, mask)
                            
                            
                            #apply the blurred circular section into the detected face area
                            blurredFace=np.where(mask!=0,blurred_circular,image)

                            #apply the blured face into the sorce image
                            image[y1:y2, x1:x2]=blurredFace[y1:y2, x1:x2]
                            
                            # if not os.path.exists(f'{BLURRED_DIR}/{dir}'):
                            #     os.mkdir(f'{BLURRED_DIR}/{dir}')
                            # cv2.imwrite(f'{BLURRED_DIR}/{dir}/{img}', image)
                            blurred_images.append(image)
                            LOGGER.info('image blurring ended')
                       
                        except cv2.error as e:
                            LOGGER.error(f"OpenCV error occurred: {e}")
                            # Handle specific OpenCV errors

                        except IndexError as e:
                            LOGGER.error(f"IndexError: {e}")
                            # Handle IndexError if facial_area doesn't have expected values

                        except Exception as e:
                            LOGGER.error(f"An unexpected error occurred: {e}")
                            # Handle any other unexpected errors
                        
    if blurred_images !=[]:
            return blurred_images
    else:
            return None

# images = ndarrays of images, fd_threshold =  face detection threshold (float), LOGGER = Logger object for creating log
def blureFace_file(image,fd_threshold,LOGGER):
        st=time.time()
        blurred_images=[]
        indexes=[]
        # for i,img in enumerate(images):
                
        LOGGER.info(f'face detection started ')
        print(f'face detection started - {time.time()-st}')
        resp = RetinaFace.detect_faces(image,threshold=fd_threshold)
        LOGGER.info(f'face detection ended  ')
        print(f'face detection ended  - {time.time()-st}')
    
        for identity in resp:
            LOGGER.info(f'image blurring started ')
            print(f'image blurring started - {time.time()-st} ')
            try:
                facial_area = resp[identity]['facial_area']   
                blurred=cv2.GaussianBlur(image,(71,71),500)

            except KeyError as e:
                # Handle KeyError (e.g., if 'facial_area' or 'identity' is not found in resp)
                LOGGER.error(f'KeyError: {str(e)}')

            except cv2.error as e:
                # Handle OpenCV errors (e.g., if there's an issue with image processing)
                LOGGER.error(f'OpenCV error: {str(e)}')

            except Exception as e:
                # Handle other unexpected errors
                LOGGER.error(f'Unexpected error: {str(e)}')

            try:     
                # Get detected face area from retinaFace response and assign face region to face veriable
                x1, y1, x2, y2 = facial_area
            
                face = image[y1:y2, x1:x2]

                #blur the face region
                
                # Create circular mask of the same size as the blurred image
                mask = np.zeros_like(blurred)
                h, w = face.shape[:2]
                center = ((x1+w//2), (y1+h//2))
                
                cv2.ellipse(mask,center,(w//2,h//2),0,0,360, (255, 255, 255), -1)
                # cv2.circle(mask, center, radius, (255, 255, 255), -1)
                # cv2.imwrite("mask.jpg",mask)
                #create a circular blurred section
                blurred_circular = cv2.bitwise_and(blurred, mask)
                
                
                #apply the blurred circular section into the detected face area
                blurredFace=np.where(mask!=0,blurred_circular,image)

                #apply the blured face into the sorce image
                image[y1:y2, x1:x2]=blurredFace[y1:y2, x1:x2]
            
            except cv2.error as e:
                LOGGER.error(f"OpenCV error occurred: {e}")
                # Handle specific OpenCV errors

            except IndexError as e:
                LOGGER.error(f"IndexError: {e}")
                # Handle IndexError if facial_area doesn't have expected values

            except Exception as e:
                LOGGER.error(f"An unexpected error occurred: {e}")
                # Handle any other unexpected errors   
        # blurred_images.append(image)
        # indexes.append(i) 
        LOGGER.info(f'image blurring ended for for image ')
        print(f'image blurring ended for for image - {time.time()-st} ')

        
        return image      




def blureFace_bytes_file(img,fd_threshold,LOGGER):
        blurred_images=[]
        indexes=[]
        
        
        st=time.time()        
        LOGGER.info(f'face detection started ')
        print(f'face detection started - {st} ')
        resp = RetinaFace.detect_faces(img,threshold=fd_threshold)
        LOGGER.info(f'face detection ended  ')
        print(f'face detection ended - {time.time()-st} ')
    
        for identity in resp:
            LOGGER.info(f'image blurring started ')
            st=time.time()
            print(f'image blurring started - {st} ')
            try:
                facial_area = resp[identity]['facial_area']   
                blurred=cv2.GaussianBlur(img,(71,71),500)

            except KeyError as e:
                # Handle KeyError (e.g., if 'facial_area' or 'identity' is not found in resp)
                LOGGER.error(f'KeyError: {str(e)}')

            except cv2.error as e:
                # Handle OpenCV errors (e.g., if there's an issue with image processing)
                LOGGER.error(f'OpenCV error: {str(e)}')

            except Exception as e:
                # Handle other unexpected errors
                LOGGER.error(f'Unexpected error: {str(e)}')

            try:     
                # Get detected face area from retinaFace response and assign face region to face veriable
                x1, y1, x2, y2 = facial_area
            
                face = img[y1:y2, x1:x2]

                #blur the face region
                
                # Create circular mask of the same size as the blurred image
                mask = np.zeros_like(blurred)
                h, w = face.shape[:2]
                center = ((x1+w//2), (y1+h//2))
                
                cv2.ellipse(mask,center,(w//2,h//2),0,0,360, (255, 255, 255), -1)
                # cv2.circle(mask, center, radius, (255, 255, 255), -1)
                # cv2.imwrite("mask.jpg",mask)
                #create a circular blurred section
                blurred_circular = cv2.bitwise_and(blurred, mask)
                
                
                #apply the blurred circular section into the detected face area
                blurredFace=np.where(mask!=0,blurred_circular,img)

                #apply the blured face into the sorce image
                img[y1:y2, x1:x2]=blurredFace[y1:y2, x1:x2]
            
            except cv2.error as e:
                LOGGER.error(f"OpenCV error occurred: {e}")
                # Handle specific OpenCV errors

            except IndexError as e:
                LOGGER.error(f"IndexError: {e}")
                # Handle IndexError if facial_area doesn't have expected values

            except Exception as e:
                LOGGER.error(f"An unexpected error occurred: {e}")
                # Handle any other unexpected errors   
        # blurred_images.append(img)
        # indexes.append(idx) 
        if resp!={}:
            LOGGER.info(f'image blurring ended for for image ')
            print(f'image blurring started - {time.time()-st} ')
            return img
        else:
            LOGGER.info(f'No faces detected')
            print(f'No faces detected - {time.time()-st} ')
            return None
            
        # if blurred_images !=[]:
        #     return blurred_images,indexes
        # else:
        #     return None



#   return image_base64
# if __name__=='__main__':
  
#    blureFace_file()
   